"""Evaluate the production BEYOND CIBIL model on the held-out 20% test dataset."""

import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, balanced_accuracy_score,
    matthews_corrcoef, log_loss, brier_score_loss
)
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# Set up paths
ARTIFACTS_DIR = Path("app/ml/artifacts")
DATASET_DIR = Path("DATASET_BEYOND_CIBIL")
OUTPUT_DIR = Path("app/ml/evaluation_output")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("BEYOND CIBIL - PRODUCTION MODEL EVALUATION")
print("=" * 80)

# ============================================================
# STEP 1: LOAD MODEL ARTIFACTS
# ============================================================
print("\n[STEP 1] Loading model artifacts...")

model = joblib.load(ARTIFACTS_DIR / "model.pkl")
scaler = joblib.load(ARTIFACTS_DIR / "scaler.pkl")
feature_columns = joblib.load(ARTIFACTS_DIR / "feature_columns.pkl")
shap_explainer = joblib.load(ARTIFACTS_DIR / "shap_explainer.pkl")

print(f"✓ Model loaded: {type(model).__name__}")
print(f"✓ Scaler loaded: {type(scaler).__name__}")
print(f"✓ Feature columns loaded: {len(feature_columns)} features")
print(f"✓ SHAP explainer loaded: {type(shap_explainer).__name__}")

# ============================================================
# STEP 2: LOAD DATASET AND RECREATE TRAIN/TEST SPLIT
# ============================================================
print("\n[STEP 2] Loading dataset and recreating train/test split...")

features_df = pd.read_csv(DATASET_DIR / "features.csv")
labels_df = pd.read_csv(DATASET_DIR / "labels.csv")

# Deduplicate (same as during training)
features_df = features_df.drop_duplicates(subset=["customer_id", "month"], keep="first")
labels_df = labels_df.drop_duplicates(subset=["customer_id", "month"], keep="first")

# Merge features and labels
merged_df = pd.merge(features_df, labels_df, on=["customer_id", "month"], how="inner")

# Engineer income_consistency feature (same as during training)
merged_df['income_consistency'] = merged_df['savings_ratio'] * merged_df['transaction_frequency']

# Select feature columns
exclude_columns = ["customer_id", "month", "repayment_probability", 
                   "alternative_credit_score", "risk_category", "repayment_label"]
X = merged_df[feature_columns].values
y = merged_df["repayment_label"].values

# Recreate train/test split (same as during training)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

print(f"✓ Dataset loaded: {len(merged_df)} samples")
print(f"✓ Train/Test split recreated: {len(X_train)} train, {len(X_test)} test")

# ============================================================
# STEP 3: VERIFY DATASET STATISTICS
# ============================================================
print("\n[STEP 3] Dataset Statistics:")
print(f"  Total samples: {len(merged_df)}")
print(f"  Training samples: {len(X_train)}")
print(f"  Testing samples: {len(X_test)}")
print(f"  Number of features: {len(feature_columns)}")
print(f"  Selected features: {feature_columns}")
print(f"  Class distribution in train: Class 0: {np.sum(y_train == 0)}, Class 1: {np.sum(y_train == 1)}")
print(f"  Class distribution in test: Class 0: {np.sum(y_test == 0)}, Class 1: {np.sum(y_test == 1)}")

# ============================================================
# STEP 4: PREPROCESS TEST DATA
# ============================================================
print("\n[STEP 4] Preprocessing test data...")

# Scale test data using fitted scaler
X_test_scaled = scaler.transform(X_test)

print(f"✓ Test data scaled")

# ============================================================
# STEP 5: GENERATE PREDICTIONS
# ============================================================
print("\n[STEP 5] Generating predictions...")

y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

print(f"✓ Predictions generated")

# ============================================================
# STEP 6: CALCULATE EVALUATION METRICS
# ============================================================
print("\n[STEP 6] Calculating evaluation metrics...")

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "f1_score": f1_score(y_test, y_pred),
    "roc_auc": roc_auc_score(y_test, y_pred_proba),
    "pr_auc": average_precision_score(y_test, y_pred_proba),
    "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
    "matthews_corrcoef": matthews_corrcoef(y_test, y_pred),
    "log_loss": log_loss(y_test, y_pred_proba),
    "brier_score": brier_score_loss(y_test, y_pred_proba)
}

print("\nEvaluation Metrics:")
for metric_name, metric_value in metrics.items():
    print(f"  {metric_name}: {metric_value:.4f}")

# ============================================================
# STEP 7: CONFUSION MATRIX
# ============================================================
print("\n[STEP 7] Confusion Matrix:")

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print(f"\n  True Negatives (TN): {tn} - Correctly predicted as High Risk")
print(f"  False Positives (FP): {fp} - Incorrectly predicted as Low Risk (Type I error)")
print(f"  False Negatives (FN): {fn} - Incorrectly predicted as High Risk (Type II error)")
print(f"  True Positives (TP): {tp} - Correctly predicted as Low Risk")

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['High Risk', 'Low Risk'],
            yticklabels=['High Risk', 'Low Risk'])
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig(OUTPUT_DIR / 'confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"✓ Confusion matrix saved to {OUTPUT_DIR / 'confusion_matrix.png'}")

# ============================================================
# STEP 8: CLASSIFICATION REPORT
# ============================================================
print("\n[STEP 8] Classification Report:")

class_report = classification_report(y_test, y_pred, output_dict=True)
print(classification_report(y_test, y_pred))

# ============================================================
# STEP 9: ROC CURVE
# ============================================================
print("\n[STEP 9] Generating ROC Curve...")

from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {metrics["roc_auc"]:.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.savefig(OUTPUT_DIR / 'roc_curve.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"✓ ROC curve saved to {OUTPUT_DIR / 'roc_curve.png'}")

# ============================================================
# STEP 10: PRECISION-RECALL CURVE
# ============================================================
print("\n[STEP 10] Generating Precision-Recall Curve...")

from sklearn.metrics import precision_recall_curve

precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='green', lw=2, label=f'PR Curve (AP = {metrics["pr_auc"]:.4f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.grid(True, alpha=0.3)
plt.savefig(OUTPUT_DIR / 'pr_curve.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"✓ Precision-Recall curve saved to {OUTPUT_DIR / 'pr_curve.png'}")

# ============================================================
# STEP 11: FEATURE IMPORTANCE
# ============================================================
print("\n[STEP 11] Feature Importance:")

feature_importance = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': feature_columns,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("\nTop 10 Feature Importances:")
for idx, row in feature_importance_df.head(10).iterrows():
    print(f"  {row['feature']}: {row['importance']:.4f}")

# Save feature importance
feature_importance_df.to_csv(OUTPUT_DIR / 'feature_importance.csv', index=False)
print(f"✓ Feature importance saved to {OUTPUT_DIR / 'feature_importance.csv'}")

# ============================================================
# STEP 12: SHAP GLOBAL IMPORTANCE
# ============================================================
print("\n[STEP 12] SHAP Global Importance:")

shap_values = shap_explainer.shap_values(X_test_scaled)
shap_importance = np.abs(shap_values).mean(axis=0)
shap_importance_df = pd.DataFrame({
    'feature': feature_columns,
    'shap_importance': shap_importance
}).sort_values('shap_importance', ascending=False)

print("\nTop 10 SHAP Global Importance:")
for idx, row in shap_importance_df.head(10).iterrows():
    print(f"  {row['feature']}: {row['shap_importance']:.4f}")

# Save SHAP importance
shap_importance_df.to_csv(OUTPUT_DIR / 'shap_importance.csv', index=False)
print(f"✓ SHAP importance saved to {OUTPUT_DIR / 'shap_importance.csv'}")

# ============================================================
# STEP 13: SHAP EXPLANATIONS FOR RANDOM SAMPLES
# ============================================================
print("\n[STEP 13] Generating SHAP explanations for 10 random test samples...")

np.random.seed(42)
random_indices = np.random.choice(len(X_test), 10, replace=False)

shap_explanations = []
for idx in random_indices:
    sample_shap_values = shap_explainer.shap_values(X_test_scaled[idx:idx+1])
    
    # Get feature contributions
    contributions = []
    for i, feature_name in enumerate(feature_columns):
        contributions.append({
            'feature': feature_name,
            'shap_value': float(sample_shap_values[0][i]),
            'feature_value': float(X_test_scaled[idx][i])
        })
    
    # Sort by absolute SHAP value
    contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)
    
    shap_explanations.append({
        'sample_index': int(idx),
        'predicted_class': int(y_pred[idx]),
        'true_class': int(y_test[idx]),
        'probability': float(y_pred_proba[idx]),
        'top_positive': [c for c in contributions if c['shap_value'] > 0][:3],
        'top_negative': [c for c in contributions if c['shap_value'] < 0][:3]
    })

print("\nSHAP Explanations for 10 Random Test Samples:")
for explanation in shap_explanations:
    print(f"\nSample {explanation['sample_index']}:")
    print(f"  Predicted Class: {explanation['predicted_class']} (True: {explanation['true_class']})")
    print(f"  Probability: {explanation['probability']:.4f}")
    print(f"  Top Positive Contributors:")
    for contrib in explanation['top_positive']:
        print(f"    {contrib['feature']}: {contrib['shap_value']:.4f}")
    print(f"  Top Negative Contributors:")
    for contrib in explanation['top_negative']:
        print(f"    {contrib['feature']}: {contrib['shap_value']:.4f}")

# Save SHAP explanations
with open(OUTPUT_DIR / 'shap_explanations.json', 'w') as f:
    json.dump(shap_explanations, f, indent=2)
print(f"✓ SHAP explanations saved to {OUTPUT_DIR / 'shap_explanations.json'}")

# ============================================================
# STEP 14: MISCLASSIFIED CASES
# ============================================================
print("\n[STEP 14] Identifying misclassified cases...")

misclassified_indices = np.where(y_pred != y_test)[0]
print(f"Total misclassified: {len(misclassified_indices)} out of {len(y_test)} ({len(misclassified_indices)/len(y_test)*100:.2f}%)")

misclassified_cases = []
for idx in misclassified_indices:
    sample_shap_values = shap_explainer.shap_values(X_test_scaled[idx:idx+1])
    
    contributions = []
    for i, feature_name in enumerate(feature_columns):
        contributions.append({
            'feature': feature_name,
            'shap_value': float(sample_shap_values[0][i])
        })
    
    contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)
    
    misclassified_cases.append({
        'sample_index': int(idx),
        'true_label': int(y_test[idx]),
        'predicted_label': int(y_pred[idx]),
        'probability': float(y_pred_proba[idx]),
        'top_contributors': contributions[:5]
    })

print("\nMisclassified Cases (first 10):")
for case in misclassified_cases[:10]:
    print(f"\nSample {case['sample_index']}:")
    print(f"  True Label: {case['true_label']}, Predicted: {case['predicted_label']}")
    print(f"  Probability: {case['probability']:.4f}")
    print(f"  Top Contributors:")
    for contrib in case['top_contributors']:
        print(f"    {contrib['feature']}: {contrib['shap_value']:.4f}")

# Save misclassified cases
with open(OUTPUT_DIR / 'misclassified_cases.json', 'w') as f:
    json.dump(misclassified_cases, f, indent=2)
print(f"✓ Misclassified cases saved to {OUTPUT_DIR / 'misclassified_cases.json'}")

# ============================================================
# STEP 15: CONFIDENCE ANALYSIS
# ============================================================
print("\n[STEP 15] Confidence Analysis...")

# Calculate confidence scores (distance from 0.5)
confidence_scores = 2 * np.abs(y_pred_proba - 0.5)

confidence_stats = {
    'average_confidence': float(np.mean(confidence_scores)),
    'min_confidence': float(np.min(confidence_scores)),
    'max_confidence': float(np.max(confidence_scores)),
    'median_confidence': float(np.median(confidence_scores))
}

print("\nConfidence Statistics:")
for stat_name, stat_value in confidence_stats.items():
    print(f"  {stat_name}: {stat_value:.4f}")

# Confidence distribution
plt.figure(figsize=(8, 6))
plt.hist(confidence_scores, bins=20, edgecolor='black', alpha=0.7)
plt.xlabel('Confidence Score')
plt.ylabel('Frequency')
plt.title('Distribution of Confidence Scores')
plt.grid(True, alpha=0.3)
plt.savefig(OUTPUT_DIR / 'confidence_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"✓ Confidence distribution saved to {OUTPUT_DIR / 'confidence_distribution.png'}")

# ============================================================
# STEP 16: SAVE ALL METRICS
# ============================================================
print("\n[STEP 16] Saving evaluation results...")

evaluation_results = {
    'dataset_statistics': {
        'total_samples': int(len(merged_df)),
        'training_samples': int(len(X_train)),
        'testing_samples': int(len(X_test)),
        'num_features': int(len(feature_columns)),
        'feature_columns': feature_columns if isinstance(feature_columns, list) else feature_columns.tolist(),
        'train_class_distribution': {
            'class_0': int(np.sum(y_train == 0)),
            'class_1': int(np.sum(y_train == 1))
        },
        'test_class_distribution': {
            'class_0': int(np.sum(y_test == 0)),
            'class_1': int(np.sum(y_test == 1))
        }
    },
    'evaluation_metrics': {k: float(v) for k, v in metrics.items()},
    'confusion_matrix': {
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'true_positives': int(tp)
    },
    'classification_report': class_report,
    'confidence_statistics': confidence_stats,
    'misclassified_count': int(len(misclassified_indices)),
    'misclassified_rate': float(len(misclassified_indices) / len(y_test))
}

with open(OUTPUT_DIR / 'evaluation_results.json', 'w') as f:
    json.dump(evaluation_results, f, indent=2)

print(f"✓ Evaluation results saved to {OUTPUT_DIR / 'evaluation_results.json'}")

print("\n" + "=" * 80)
print("EVALUATION COMPLETE")
print("=" * 80)
print(f"\nAll results saved to: {OUTPUT_DIR}")
