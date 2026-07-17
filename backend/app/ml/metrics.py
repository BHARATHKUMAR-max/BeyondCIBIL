"""Metric calculation functions for model evaluation."""

import logging
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculates various classification metrics."""

    @staticmethod
    def calculate_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate accuracy score."""
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def calculate_precision(y_true: np.ndarray, y_pred: np.ndarray, average: str = "binary") -> float:
        """Calculate precision score."""
        return precision_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def calculate_recall(y_true: np.ndarray, y_pred: np.ndarray, average: str = "binary") -> float:
        """Calculate recall score."""
        return recall_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def calculate_f1_score(y_true: np.ndarray, y_pred: np.ndarray, average: str = "binary") -> float:
        """Calculate F1 score."""
        return f1_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def calculate_roc_auc(y_true: np.ndarray, y_proba: np.ndarray) -> float:
        """Calculate ROC-AUC score."""
        try:
            return roc_auc_score(y_true, y_proba)
        except ValueError as e:
            logger.warning(f"Could not calculate ROC-AUC: {e}")
            return 0.0

    @staticmethod
    def calculate_pr_auc(y_true: np.ndarray, y_proba: np.ndarray) -> float:
        """Calculate Precision-Recall AUC score using average_precision_score."""
        try:
            return average_precision_score(y_true, y_proba)
        except ValueError as e:
            logger.warning(f"Could not calculate PR-AUC: {e}")
            return 0.0

    @staticmethod
    def calculate_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """Calculate confusion matrix."""
        return confusion_matrix(y_true, y_pred)

    @staticmethod
    def calculate_all_metrics(
        y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray
    ) -> dict[str, Any]:
        """Calculate all classification metrics."""
        metrics = {
            "accuracy": MetricsCalculator.calculate_accuracy(y_true, y_pred),
            "precision": MetricsCalculator.calculate_precision(y_true, y_pred),
            "recall": MetricsCalculator.calculate_recall(y_true, y_pred),
            "f1_score": MetricsCalculator.calculate_f1_score(y_true, y_pred),
            "roc_auc": MetricsCalculator.calculate_roc_auc(y_true, y_proba),
            "pr_auc": MetricsCalculator.calculate_pr_auc(y_true, y_proba),
        }
        return metrics

    @staticmethod
    def get_classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> str:
        """Generate classification report."""
        return classification_report(y_true, y_pred)

    @staticmethod
    def get_roc_curve_data(y_true: np.ndarray, y_proba: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get ROC curve data."""
        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        return fpr, tpr, thresholds

    @staticmethod
    def get_pr_curve_data(y_true: np.ndarray, y_proba: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get Precision-Recall curve data."""
        precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
        return precision, recall, thresholds
