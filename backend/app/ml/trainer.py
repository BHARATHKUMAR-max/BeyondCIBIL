"""Model training orchestration."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.ml.evaluation import ModelEvaluator
from app.ml.model_selection import ModelSelector
from app.ml.pipeline import MLPipeline
from app.ml.visualization import ModelVisualizer

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Orchestrates the complete model training pipeline."""

    def __init__(
        self,
        artifacts_dir: Path = Path("app/ml/artifacts"),
        test_size: float = 0.2,
        random_state: int = 42,
        use_hyperparameter_tuning: bool = True,
    ):
        """Initialize model trainer."""
        self.artifacts_dir = Path(artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.test_size = test_size
        self.random_state = random_state
        self.use_hyperparameter_tuning = use_hyperparameter_tuning

        self.ml_pipeline = MLPipeline()
        self.model_selector = ModelSelector(random_state=random_state)
        self.scaler = StandardScaler()
        self.model = None
        self.feature_columns = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.evaluator = None
        self.visualizer = None

    def load_and_prepare_data(self) -> tuple[np.ndarray, np.ndarray, list[str]]:
        """Load data using ML pipeline and prepare for training."""
        logger.info("Loading and preparing data")

        # Load features and labels directly from existing CSV files
        from app.ml.dataset_loader import DatasetLoader

        loader = DatasetLoader()
        features_df = loader.load_features()
        labels_df = loader.load_labels()

        logger.info(f"Loaded features: {len(features_df)} rows")
        logger.info(f"Loaded labels: {len(labels_df)} rows")

        # Merge features with labels on customer_id
        merged_df = pd.merge(features_df, labels_df, on="customer_id", how="inner")
        logger.info(f"Merged dataset: {len(merged_df)} rows")

        # Extract feature columns (exclude customer_id, month, and label columns)
        exclude_columns = ["customer_id", "month", "repayment_probability", "alternative_credit_score", "risk_category", "repayment_label"]
        self.feature_columns = [col for col in merged_df.columns if col not in exclude_columns]
        
        # Select only numeric columns
        numeric_columns = merged_df[self.feature_columns].select_dtypes(include=[np.number]).columns.tolist()
        self.feature_columns = numeric_columns
        
        X = merged_df[self.feature_columns].values
        y = merged_df["repayment_label"].values

        logger.info(f"Data prepared: X shape {X.shape}, y shape {y.shape}")
        logger.info(f"Feature columns: {len(self.feature_columns)}")
        logger.info(f"Label distribution: Class 0: {np.sum(y == 0)}, Class 1: {np.sum(y == 1)}")

        return X, y, self.feature_columns

    def _generate_synthetic_labels(self, X: np.ndarray) -> np.ndarray:
        """Generate synthetic labels based on feature patterns."""
        # Create a simple rule-based label for demonstration
        # In production, this would come from actual labels
        np.random.seed(self.random_state)

        # Use a combination of features to create somewhat realistic labels
        # Assuming features are normalized, create probability based on first few features
        if X.shape[1] > 0:
            score = np.sum(X[:, :3], axis=1) + np.random.normal(0, 0.5, X.shape[0])
            probability = 1 / (1 + np.exp(-score))  # sigmoid
            y = (probability > 0.5).astype(int)
        else:
            y = np.random.randint(0, 2, X.shape[0])

        return y

    def split_data(self, X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split data into train and test sets using stratified split."""
        logger.info(f"Splitting data with test_size={self.test_size}")

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        logger.info(f"Train set: {self.X_train.shape[0]} samples")
        logger.info(f"Test set: {self.X_test.shape[0]} samples")

        return self.X_train, self.X_test, self.y_train, self.y_test

    def scale_features(self) -> tuple[np.ndarray, np.ndarray]:
        """Scale features using StandardScaler."""
        logger.info("Scaling features")

        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

        logger.info("Feature scaling completed")
        return self.X_train, self.X_test

    def train_model(self) -> Any:
        """Train the model with or without hyperparameter tuning."""
        logger.info("Training model")

        if self.use_hyperparameter_tuning:
            logger.info("Using hyperparameter tuning")
            self.model = self.model_selector.randomized_search_cv(
                self.X_train, self.y_train, n_iter=50, cv=5, scoring="roc_auc"
            )
        else:
            logger.info("Using default parameters")
            self.model = self.model_selector.train_with_default_params(self.X_train, self.y_train)

        logger.info("Model training completed")
        return self.model

    def evaluate_model(self) -> dict[str, Any]:
        """Evaluate the trained model."""
        logger.info("Evaluating model")

        self.evaluator = ModelEvaluator(self.model, self.X_test, self.y_test, self.feature_columns)
        metrics = self.evaluator.evaluate()

        # Calculate SHAP values for interpretability
        logger.info("Calculating SHAP values")
        self.evaluator.calculate_shap_values()

        logger.info(f"Model evaluation completed: Accuracy={metrics['accuracy']:.4f}, ROC-AUC={metrics['roc_auc']:.4f}")
        return metrics

    def generate_visualizations(self) -> dict[str, Path]:
        """Generate all visualization plots."""
        logger.info("Generating visualizations")

        self.visualizer = ModelVisualizer(self.evaluator.metrics, self.artifacts_dir)

        feature_importance = self.evaluator.calculate_feature_importance()
        permutation_importance = self.evaluator.calculate_permutation_importance()

        saved_plots = self.visualizer.generate_all_plots(feature_importance, permutation_importance)

        logger.info(f"Visualizations generated: {len(saved_plots)} plots")
        return saved_plots

    def save_artifacts(self) -> dict[str, Path]:
        """Save all training artifacts."""
        logger.info(f"Saving artifacts to {self.artifacts_dir}")

        saved_artifacts = {}

        # Save model
        model_path = self.artifacts_dir / "model.joblib"
        joblib.dump(self.model, model_path)
        saved_artifacts["model"] = model_path

        # Save scaler
        scaler_path = self.artifacts_dir / "scaler.joblib"
        joblib.dump(self.scaler, scaler_path)
        saved_artifacts["scaler"] = scaler_path

        # Save feature columns
        feature_columns_path = self.artifacts_dir / "feature_columns.joblib"
        joblib.dump(self.feature_columns, feature_columns_path)
        saved_artifacts["feature_columns"] = feature_columns_path

        # Save evaluation results
        if self.evaluator:
            evaluation_artifacts = self.evaluator.save_evaluation_results(self.artifacts_dir)
            saved_artifacts.update(evaluation_artifacts)

        logger.info(f"Artifacts saved: {list(saved_artifacts.keys())}")
        return saved_artifacts

    def generate_training_report(self) -> Path:
        """Generate training report in markdown format."""
        logger.info("Generating training report")

        report_path = self.artifacts_dir / "training_report.md"

        with open(report_path, "w") as f:
            f.write("# Model Training Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Dataset Summary
            f.write("## Dataset Summary\n\n")
            f.write(f"- **Training samples:** {len(self.X_train)}\n")
            f.write(f"- **Test samples:** {len(self.X_test)}\n")
            f.write(f"- **Features:** {len(self.feature_columns)}\n")
            f.write(f"- **Feature columns:** {', '.join(self.feature_columns[:10])}...\n\n")

            # Model Configuration
            f.write("## Model Configuration\n\n")
            f.write("- **Model:** XGBoost Classifier\n")
            f.write(f"- **Hyperparameter tuning:** {'Enabled' if self.use_hyperparameter_tuning else 'Disabled'}\n\n")

            if self.model_selector.best_params:
                f.write("### Best Hyperparameters\n\n")
                for param, value in self.model_selector.best_params.items():
                    f.write(f"- **{param}:** {value}\n")
                f.write("\n")

            # Metrics
            f.write("## Model Performance Metrics\n\n")
            if self.evaluator:
                metrics = self.evaluator.metrics
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                f.write(f"| Accuracy | {metrics['accuracy']:.4f} |\n")
                f.write(f"| Precision | {metrics['precision']:.4f} |\n")
                f.write(f"| Recall | {metrics['recall']:.4f} |\n")
                f.write(f"| F1 Score | {metrics['f1_score']:.4f} |\n")
                f.write(f"| ROC-AUC | {metrics['roc_auc']:.4f} |\n")
                f.write(f"| PR-AUC | {metrics['pr_auc']:.4f} |\n\n")

                # Confusion Matrix
                f.write("### Confusion Matrix\n\n")
                cm = metrics["confusion_matrix"]
                f.write("```\n")
                f.write(f"              Predicted\n")
                f.write(f"Actual    TN={cm[0,0]}    FP={cm[0,1]}\n")
                f.write(f"          FN={cm[1,0]}    TP={cm[1,1]}\n")
                f.write("```\n\n")

                # Classification Report
                f.write("### Classification Report\n\n")
                f.write("```\n")
                f.write(metrics["classification_report"])
                f.write("```\n\n")

                # Feature Importance
                f.write("## Feature Importance\n\n")
                feature_importance = self.evaluator.calculate_feature_importance()
                f.write("| Feature | Importance |\n")
                f.write("|---------|------------|\n")
                for feature, importance in list(feature_importance.items())[:15]:
                    f.write(f"| {feature} | {importance:.4f} |\n")
                f.write("\n")

            # Artifacts
            f.write("## Saved Artifacts\n\n")
            f.write("The following artifacts have been saved:\n\n")
            f.write("- `model.joblib` - Trained XGBoost model\n")
            f.write("- `scaler.joblib` - Fitted StandardScaler\n")
            f.write("- `feature_columns.joblib` - Feature column names\n")
            f.write("- `shap_explainer.joblib` - SHAP explainer\n")
            f.write("- `metrics.joblib` - Evaluation metrics\n")
            f.write("- `feature_importance.csv` - Feature importance values\n")
            f.write("- `permutation_importance.csv` - Permutation importance values\n\n")

            # Visualizations
            f.write("## Visualizations\n\n")
            f.write("The following visualizations have been generated:\n\n")
            f.write("- `confusion_matrix.png` - Confusion matrix heatmap\n")
            f.write("- `roc_curve.png` - ROC curve\n")
            f.write("- `pr_curve.png` - Precision-Recall curve\n")
            f.write("- `feature_importance.png` - Feature importance bar chart\n")
            f.write("- `permutation_importance.png` - Permutation importance bar chart\n")
            f.write("- `metrics_comparison.png` - Metrics comparison chart\n\n")

        logger.info(f"Training report saved to {report_path}")
        return report_path

    def run_training_pipeline(self) -> dict[str, Any]:
        """Run the complete training pipeline."""
        logger.info("=" * 50)
        logger.info("Starting Model Training Pipeline")
        logger.info("=" * 50)

        results = {}

        try:
            # Step 1: Load and prepare data
            X, y, feature_columns = self.load_and_prepare_data()
            results["data_loaded"] = True

            # Step 2: Split data
            self.split_data(X, y)
            results["data_split"] = True

            # Step 3: Scale features
            self.scale_features()
            results["features_scaled"] = True

            # Step 4: Train model
            self.train_model()
            results["model_trained"] = True

            # Step 5: Evaluate model
            metrics = self.evaluate_model()
            results["metrics"] = metrics
            results["model_evaluated"] = True

            # Step 6: Generate visualizations
            visualizations = self.generate_visualizations()
            results["visualizations"] = list(visualizations.keys())
            results["visualizations_generated"] = True

            # Step 7: Save artifacts
            artifacts = self.save_artifacts()
            results["artifacts"] = list(artifacts.keys())
            results["artifacts_saved"] = True

            # Step 8: Generate training report
            report_path = self.generate_training_report()
            results["report_path"] = str(report_path)
            results["report_generated"] = True

            logger.info("=" * 50)
            logger.info("Training Pipeline Completed Successfully")
            logger.info("=" * 50)

            return results

        except Exception as e:
            logger.error(f"Training pipeline failed: {str(e)}")
            results["success"] = False
            results["error"] = str(e)
            return results
