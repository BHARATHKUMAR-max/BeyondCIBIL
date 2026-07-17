"""Visualization functions for model evaluation."""

import logging
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

logger = logging.getLogger(__name__)


class ModelVisualizer:
    """Creates visualizations for model evaluation results."""

    def __init__(self, metrics: dict[str, Any], output_dir: Path):
        """Initialize visualizer with metrics and output directory."""
        self.metrics = metrics
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams["figure.figsize"] = (10, 6)

    def plot_confusion_matrix(self, save: bool = True) -> plt.Figure:
        """Plot confusion matrix."""
        cm = self.metrics["confusion_matrix"]
        fig, ax = plt.subplots()

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax,
            xticklabels=["Negative", "Positive"],
            yticklabels=["Negative", "Positive"],
        )
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")

        if save:
            path = self.output_dir / "confusion_matrix.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"Confusion matrix saved to {path}")
            plt.close(fig)

        return fig

    def plot_roc_curve(self, save: bool = True) -> plt.Figure:
        """Plot ROC curve."""
        roc_data = self.metrics["roc_curve"]
        fpr = roc_data["fpr"]
        tpr = roc_data["tpr"]
        auc = self.metrics["roc_auc"]

        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.4f})", linewidth=2)
        ax.plot([0, 1], [0, 1], "k--", label="Random Classifier")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save:
            path = self.output_dir / "roc_curve.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"ROC curve saved to {path}")
            plt.close(fig)

        return fig

    def plot_precision_recall_curve(self, save: bool = True) -> plt.Figure:
        """Plot Precision-Recall curve."""
        pr_data = self.metrics["pr_curve"]
        precision = pr_data["precision"]
        recall = pr_data["recall"]
        auc = self.metrics["pr_auc"]

        fig, ax = plt.subplots()
        ax.plot(recall, precision, label=f"PR Curve (AUC = {auc:.4f})", linewidth=2)
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save:
            path = self.output_dir / "pr_curve.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"PR curve saved to {path}")
            plt.close(fig)

        return fig

    def plot_feature_importance(self, feature_importance: dict[str, float], top_n: int = 20, save: bool = True) -> plt.Figure:
        """Plot feature importance."""
        # Sort and take top N
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        features, importances = zip(*sorted_features)

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(range(len(features)), importances, color="steelblue")
        ax.set_yticks(range(len(features)))
        ax.set_yticklabels(features)
        ax.set_xlabel("Importance")
        ax.set_title(f"Top {top_n} Feature Importance")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis="x")

        if save:
            path = self.output_dir / "feature_importance.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"Feature importance plot saved to {path}")
            plt.close(fig)

        return fig

    def plot_permutation_importance(
        self, permutation_importance: dict[str, float], top_n: int = 20, save: bool = True
    ) -> plt.Figure:
        """Plot permutation importance."""
        # Sort and take top N
        sorted_features = sorted(permutation_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        features, importances = zip(*sorted_features)

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(range(len(features)), importances, color="coral")
        ax.set_yticks(range(len(features)))
        ax.set_yticklabels(features)
        ax.set_xlabel("Mean Decrease in Accuracy")
        ax.set_title(f"Top {top_n} Permutation Importance")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis="x")

        if save:
            path = self.output_dir / "permutation_importance.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"Permutation importance plot saved to {path}")
            plt.close(fig)

        return fig

    def plot_shap_summary(self, shap_values: np.ndarray, feature_names: list[str], save: bool = True) -> plt.Figure:
        """Plot SHAP summary plot."""
        try:
            import shap

            fig, ax = plt.subplots(figsize=(12, 8))
            shap.summary_plot(shap_values, feature_names=feature_names, plot_type="bar", show=False)
            ax.set_title("SHAP Feature Importance")

            if save:
                path = self.output_dir / "shap_summary.png"
                fig.savefig(path, dpi=300, bbox_inches="tight")
                logger.info(f"SHAP summary plot saved to {path}")
                plt.close(fig)

            return fig
        except ImportError:
            logger.warning("SHAP not installed, skipping SHAP summary plot")
            return None

    def plot_shap_beeswarm(self, shap_values: np.ndarray, X_test: np.ndarray, feature_names: list[str], save: bool = True) -> plt.Figure:
        """Plot SHAP beeswarm plot."""
        try:
            import shap

            fig, ax = plt.subplots(figsize=(12, 8))
            shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
            ax.set_title("SHAP Beeswarm Plot")

            if save:
                path = self.output_dir / "shap_beeswarm.png"
                fig.savefig(path, dpi=300, bbox_inches="tight")
                logger.info(f"SHAP beeswarm plot saved to {path}")
                plt.close(fig)

            return fig
        except ImportError:
            logger.warning("SHAP not installed, skipping SHAP beeswarm plot")
            return None

    def plot_metrics_comparison(self, save: bool = True) -> plt.Figure:
        """Plot comparison of all metrics."""
        metric_names = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC", "PR-AUC"]
        metric_values = [
            self.metrics["accuracy"],
            self.metrics["precision"],
            self.metrics["recall"],
            self.metrics["f1_score"],
            self.metrics["roc_auc"],
            self.metrics["pr_auc"],
        ]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(metric_names, metric_values, color=["steelblue"] * 6)
        ax.set_ylabel("Score")
        ax.set_title("Model Metrics Comparison")
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis="y")

        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{value:.4f}", ha="center", va="bottom")

        if save:
            path = self.output_dir / "metrics_comparison.png"
            fig.savefig(path, dpi=300, bbox_inches="tight")
            logger.info(f"Metrics comparison plot saved to {path}")
            plt.close(fig)

        return fig

    def generate_all_plots(
        self, feature_importance: dict[str, float], permutation_importance: dict[str, float] | None = None
    ) -> dict[str, Path]:
        """Generate all visualization plots."""
        logger.info("Generating all visualization plots")

        saved_plots = {}

        # Basic evaluation plots
        self.plot_confusion_matrix()
        saved_plots["confusion_matrix"] = self.output_dir / "confusion_matrix.png"

        self.plot_roc_curve()
        saved_plots["roc_curve"] = self.output_dir / "roc_curve.png"

        self.plot_precision_recall_curve()
        saved_plots["pr_curve"] = self.output_dir / "pr_curve.png"

        self.plot_metrics_comparison()
        saved_plots["metrics_comparison"] = self.output_dir / "metrics_comparison.png"

        # Feature importance plots
        self.plot_feature_importance(feature_importance)
        saved_plots["feature_importance"] = self.output_dir / "feature_importance.png"

        if permutation_importance:
            self.plot_permutation_importance(permutation_importance)
            saved_plots["permutation_importance"] = self.output_dir / "permutation_importance.png"

        logger.info("All visualization plots generated")
        return saved_plots
