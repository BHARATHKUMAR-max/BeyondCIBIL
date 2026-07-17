"""Model selection and hyperparameter tuning."""

import logging
from typing import Any

import numpy as np
from sklearn.model_selection import RandomizedSearchCV, StratifiedShuffleSplit
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)


class ModelSelector:
    """Handles model selection and hyperparameter tuning."""

    def __init__(self, random_state: int = 42, n_jobs: int = -1):
        """Initialize model selector."""
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.best_model = None
        self.best_params = None
        self.best_score = None
        self.search_results = None

    def get_xgboost_model(self, **kwargs) -> XGBClassifier:
        """Get XGBoost classifier with default parameters."""
        default_params = {
            "random_state": self.random_state,
            "n_jobs": self.n_jobs,
            "eval_metric": "logloss",
            "use_label_encoder": False,
        }
        default_params.update(kwargs)
        return XGBClassifier(**default_params)

    def get_hyperparameter_space(self) -> dict[str, Any]:
        """Get hyperparameter search space for XGBoost."""
        return {
            "n_estimators": [100, 200, 300, 400, 500],
            "max_depth": [3, 4, 5, 6, 7, 8, 9, 10],
            "learning_rate": [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
            "min_child_weight": [1, 3, 5, 7, 9],
            "gamma": [0, 0.1, 0.2, 0.3, 0.4, 0.5],
            "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
            "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
            "reg_alpha": [0, 0.01, 0.1, 1, 10],
            "reg_lambda": [0, 0.01, 0.1, 1, 10],
        }

    def randomized_search_cv(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        n_iter: int = 50,
        cv: int = 5,
        scoring: str = "roc_auc",
        verbose: int = 1,
    ) -> XGBClassifier:
        """Perform RandomizedSearchCV for hyperparameter tuning."""
        logger.info("Starting RandomizedSearchCV for hyperparameter tuning")

        model = self.get_xgboost_model()
        param_distributions = self.get_hyperparameter_space()

        # Use StratifiedShuffleSplit for consistent stratified splitting
        cv_splitter = StratifiedShuffleSplit(n_splits=cv, test_size=0.2, random_state=self.random_state)

        random_search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_distributions,
            n_iter=n_iter,
            cv=cv_splitter,
            scoring=scoring,
            random_state=self.random_state,
            n_jobs=self.n_jobs,
            verbose=verbose,
            return_train_score=True,
        )

        random_search.fit(X_train, y_train)

        self.best_model = random_search.best_estimator_
        self.best_params = random_search.best_params_
        self.best_score = random_search.best_score_
        self.search_results = random_search.cv_results_

        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best {scoring} score: {self.best_score:.4f}")

        return self.best_model

    def train_with_default_params(
        self, X_train: np.ndarray, y_train: np.ndarray
    ) -> XGBClassifier:
        """Train model with default parameters."""
        logger.info("Training model with default parameters")

        model = self.get_xgboost_model(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            min_child_weight=1,
            gamma=0,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0,
            reg_lambda=1,
        )

        model.fit(X_train, y_train)
        self.best_model = model
        self.best_params = model.get_params()
        self.best_score = None

        logger.info("Model training completed with default parameters")
        return model

    def get_feature_importance(self) -> dict[str, float]:
        """Get feature importance from the best model."""
        if self.best_model is None:
            raise ValueError("Model has not been trained yet")

        importances = self.best_model.feature_importances_
        return dict(enumerate(importances))

    def get_search_results_summary(self) -> dict[str, Any]:
        """Get summary of search results."""
        if self.search_results is None:
            return {}

        summary = {
            "best_params": self.best_params,
            "best_score": self.best_score,
            "mean_test_score": np.mean(self.search_results["mean_test_score"]),
            "std_test_score": np.std(self.search_results["mean_test_score"]),
            "mean_fit_time": np.mean(self.search_results["mean_fit_time"]),
            "total_iterations": len(self.search_results["params"]),
        }

        return summary
