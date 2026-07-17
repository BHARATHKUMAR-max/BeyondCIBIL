"""Model evaluation logic."""

import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import shap

from app.ml.metrics import MetricsCalculator

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluates trained models and generates insights."""

    def __init__(self, model: Any, X_test: np.ndarray, y_test: np.ndarray, feature_names: list[str]):
        """Initialize evaluator with model and test data."""
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.feature_names = feature_names
        self.y_pred = None
        self.y_proba = None
        self.metrics = {}
        self.shap_values = None
        self.explainer = None

    def evaluate(self) -> dict[str, Any]:
        """Run complete evaluation."""
        logger.info("Starting model evaluation")

        # Generate predictions
        self.y_pred = self.model.predict(self.X_test)
        self.y_proba = self.model.predict_proba(self.X_test)[:, 1]

        # Calculate metrics
        self.metrics = MetricsCalculator.calculate_all_metrics(self.y_test, self.y_pred, self.y_proba)

        # Calculate confusion matrix
        self.metrics["confusion_matrix"] = MetricsCalculator.calculate_confusion_matrix(self.y_test, self.y_pred)

        # Generate classification report
        self.metrics["classification_report"] = MetricsCalculator.get_classification_report(self.y_test, self.y_pred)

        # Get ROC curve data
        fpr, tpr, thresholds = MetricsCalculator.get_roc_curve_data(self.y_test, self.y_proba)
        self.metrics["roc_curve"] = {"fpr": fpr, "tpr": tpr, "thresholds": thresholds}

        # Get PR curve data
        precision, recall, thresholds = MetricsCalculator.get_pr_curve_data(self.y_test, self.y_proba)
        self.metrics["pr_curve"] = {"precision": precision, "recall": recall, "thresholds": thresholds}

        logger.info("Model evaluation completed")
        return self.metrics

    def calculate_feature_importance(self) -> dict[str, float]:
        """Calculate XGBoost feature importance."""
        importances = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importances))
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

    def calculate_permutation_importance(self, n_repeats: int = 5) -> dict[str, float]:
        """Calculate permutation importance."""
        from sklearn.inspection import permutation_importance

        result = permutation_importance(
            self.model, self.X_test, self.y_test, n_repeats=n_repeats, random_state=42, n_jobs=-1
        )

        importance_dict = dict(zip(self.feature_names, result.importances_mean))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))

    def calculate_shap_values(self, max_samples: int = 100) -> tuple[Any, Any]:
        """Calculate SHAP values for model interpretability."""
        logger.info("Calculating SHAP values")

        # Use TreeExplainer for XGBoost
        self.explainer = shap.TreeExplainer(self.model)

        # Sample data if too large
        if len(self.X_test) > max_samples:
            sample_indices = np.random.choice(len(self.X_test), max_samples, replace=False)
            X_sample = self.X_test[sample_indices]
        else:
            X_sample = self.X_test

        self.shap_values = self.explainer.shap_values(X_sample)

        logger.info("SHAP values calculated")
        return self.explainer, self.shap_values

    def get_feature_importance_df(self) -> pd.DataFrame:
        """Get feature importance as DataFrame."""
        importance_dict = self.calculate_feature_importance()
        df = pd.DataFrame.from_dict(importance_dict, orient="index", columns=["importance"])
        df = df.sort_values("importance", ascending=False)
        return df

    def get_permutation_importance_df(self, n_repeats: int = 5) -> pd.DataFrame:
        """Get permutation importance as DataFrame."""
        importance_dict = self.calculate_permutation_importance(n_repeats)
        df = pd.DataFrame.from_dict(importance_dict, orient="index", columns=["importance"])
        df = df.sort_values("importance", ascending=False)
        return df

    def get_shap_summary_df(self) -> pd.DataFrame:
        """Get SHAP summary as DataFrame."""
        if self.shap_values is None:
            self.calculate_shap_values()

        shap_mean = np.abs(self.shap_values).mean(axis=0)
        df = pd.DataFrame({"feature": self.feature_names, "shap_importance": shap_mean})
        df = df.sort_values("shap_importance", ascending=False)
        return df

    def save_evaluation_results(self, output_dir: Path) -> dict[str, Path]:
        """Save evaluation results to files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = {}

        # Save metrics
        metrics_path = output_dir / "metrics.joblib"
        joblib.dump(self.metrics, metrics_path)
        saved_files["metrics"] = metrics_path

        # Save feature importance
        feature_importance_df = self.get_feature_importance_df()
        feature_importance_path = output_dir / "feature_importance.csv"
        feature_importance_df.to_csv(feature_importance_path)
        saved_files["feature_importance"] = feature_importance_path

        # Save permutation importance
        permutation_importance_df = self.get_permutation_importance_df()
        permutation_importance_path = output_dir / "permutation_importance.csv"
        permutation_importance_df.to_csv(permutation_importance_path)
        saved_files["permutation_importance"] = permutation_importance_path

        # Save SHAP explainer and values
        if self.explainer is not None:
            explainer_path = output_dir / "shap_explainer.joblib"
            joblib.dump(self.explainer, explainer_path)
            saved_files["shap_explainer"] = explainer_path

            shap_values_path = output_dir / "shap_values.joblib"
            joblib.dump(self.shap_values, shap_values_path)
            saved_files["shap_values"] = shap_values_path

        logger.info(f"Evaluation results saved to {output_dir}")
        return saved_files
