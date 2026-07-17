"""End-to-end ML pipeline orchestration."""

import logging
from typing import Any

import pandas as pd

from app.ml.config import ml_config
from app.ml.dataset_loader import DatasetLoader
from app.ml.feature_engineering import FeatureEngineer
from app.ml.preprocessing import DataPreprocessor
from app.ml.schemas import PipelineResult
from app.ml.validation import DataValidator

logger = logging.getLogger(__name__)


class MLPipeline:
    """Orchestrates the complete ML pipeline from raw data to feature matrix."""

    def __init__(self, config: Any = ml_config):
        """Initialize ML pipeline with configuration."""
        self.config = config
        self.loader = DatasetLoader(config)
        self.validator = DataValidator(config)
        self.preprocessor = DataPreprocessor(config)
        self.feature_engineer = FeatureEngineer(config)

    def run(
        self,
        validate: bool = True,
        clean: bool = True,
        engineer: bool = True,
    ) -> PipelineResult:
        """Run the complete ML pipeline."""
        logger.info("Starting ML pipeline execution")
        errors = []
        metadata = {}

        try:
            # Step 1: Load datasets
            logger.info("Step 1: Loading datasets")
            datasets = self.loader.load_all()
            transactions_df = datasets["transactions"]
            customers_df = datasets["customers"]
            features_df = datasets["features"]
            labels_df = datasets["labels"]

            metadata["raw_transaction_count"] = len(transactions_df)
            metadata["raw_customer_count"] = len(customers_df)

            # Step 2: Validate datasets
            if validate:
                logger.info("Step 2: Validating datasets")
                transactions_validation = self.validator.validate_transactions(transactions_df)
                customers_validation = self.validator.validate_customers(customers_df)

                if not transactions_validation.is_valid:
                    errors.extend(transactions_validation.errors)
                    logger.error(f"Transactions validation failed: {transactions_validation.errors}")

                if not customers_validation.is_valid:
                    errors.extend(customers_validation.errors)
                    logger.error(f"Customers validation failed: {customers_validation.errors}")

                if errors:
                    return PipelineResult(
                        success=False,
                        errors=errors,
                        metadata=metadata,
                    )

                metadata["validation_passed"] = True

            # Step 3: Preprocess/Clean data
            if clean:
                logger.info("Step 3: Preprocessing data")
                transactions_cleaned = self.preprocessor.clean_transactions(transactions_df)
                customers_cleaned = self.preprocessor.clean_customers(customers_df)

                metadata["cleaned_transaction_count"] = len(transactions_cleaned)
                metadata["cleaned_customer_count"] = len(customers_cleaned)
            else:
                transactions_cleaned = transactions_df
                customers_cleaned = customers_df

            # Step 4: Feature Engineering
            if engineer:
                logger.info("Step 4: Engineering features")
                feature_matrix = self.feature_engineer.engineer_features(transactions_cleaned)

                metadata["feature_matrix_shape"] = feature_matrix.shape
                metadata["feature_count"] = len(feature_matrix.columns) - 1  # Exclude customer_id
            else:
                feature_matrix = transactions_cleaned

            # Step 5: Prepare labels if available
            if not labels_df.empty:
                logger.info("Step 5: Preparing labels")
                # Use repayment_label if available, otherwise fallback to label
                label_column = "repayment_label" if "repayment_label" in labels_df.columns else "label"
                labels = labels_df.set_index("customer_id")[label_column].to_dict()
                metadata["label_count"] = len(labels)
            else:
                labels = {}
                metadata["label_count"] = 0

            logger.info("ML pipeline completed successfully")

            return PipelineResult(
                success=True,
                feature_matrix=feature_matrix.to_dict(orient="records") if isinstance(feature_matrix, pd.DataFrame) else feature_matrix,
                labels=labels,
                metadata=metadata,
                errors=errors,
            )

        except Exception as e:
            logger.error(f"ML pipeline failed: {str(e)}")
            errors.append(f"Pipeline execution error: {str(e)}")
            return PipelineResult(
                success=False,
                errors=errors,
                metadata=metadata,
            )

    def run_for_customer(self, customer_id: str) -> PipelineResult:
        """Run pipeline for a single customer."""
        logger.info(f"Running ML pipeline for customer {customer_id}")
        errors = []
        metadata = {"customer_id": customer_id}

        try:
            # Load transactions for specific customer
            transactions_df = self.loader.load_transactions_for_customer(customer_id)

            if transactions_df.empty:
                errors.append(f"No transactions found for customer {customer_id}")
                return PipelineResult(success=False, errors=errors, metadata=metadata)

            metadata["transaction_count"] = len(transactions_df)

            # Validate
            validation = self.validator.validate_transactions(transactions_df)
            if not validation.is_valid:
                errors.extend(validation.errors)
                return PipelineResult(success=False, errors=errors, metadata=metadata)

            # Clean
            transactions_cleaned = self.preprocessor.clean_transactions(transactions_df)

            # Engineer features
            feature_matrix = self.feature_engineer.engineer_features(transactions_cleaned)

            if feature_matrix.empty:
                errors.append(f"Could not engineer features for customer {customer_id}")
                return PipelineResult(success=False, errors=errors, metadata=metadata)

            logger.info(f"Pipeline completed for customer {customer_id}")

            return PipelineResult(
                success=True,
                feature_matrix=feature_matrix.iloc[0].to_dict(),
                metadata=metadata,
                errors=errors,
            )

        except Exception as e:
            logger.error(f"Pipeline failed for customer {customer_id}: {str(e)}")
            errors.append(f"Pipeline execution error: {str(e)}")
            return PipelineResult(success=False, errors=errors, metadata=metadata)

    def get_feature_matrix(self) -> pd.DataFrame:
        """Get feature matrix for all customers (convenience method)."""
        result = self.run(validate=False, clean=True, engineer=True)
        if result.success and result.feature_matrix:
            return pd.DataFrame(result.feature_matrix)
        return pd.DataFrame()

    def get_customer_features(self, customer_id: str) -> dict[str, Any] | None:
        """Get features for a specific customer (convenience method)."""
        result = self.run_for_customer(customer_id)
        if result.success and result.feature_matrix:
            return result.feature_matrix
        return None

    def validate_pipeline(self) -> dict[str, Any]:
        """Validate pipeline components without full execution."""
        logger.info("Validating pipeline components")
        validation_results = {}

        try:
            # Test dataset loading
            datasets = self.loader.load_all()
            validation_results["dataset_loading"] = {
                "success": True,
                "transactions_count": len(datasets["transactions"]),
                "customers_count": len(datasets["customers"]),
            }

            # Test validation
            transactions_validation = self.validator.validate_transactions(datasets["transactions"])
            customers_validation = self.validator.validate_customers(datasets["customers"])
            validation_results["validation"] = {
                "transactions_valid": transactions_validation.is_valid,
                "customers_valid": customers_validation.is_valid,
                "transactions_errors": transactions_validation.errors,
                "customers_errors": customers_validation.errors,
            }

            # Test preprocessing
            preprocessed = self.preprocessor.clean_transactions(datasets["transactions"])
            validation_results["preprocessing"] = {
                "success": True,
                "preprocessed_count": len(preprocessed),
            }

            # Test feature engineering (on sample)
            if len(preprocessed) >= self.config.min_transactions_for_features:
                sample_customer = preprocessed["customer_id"].iloc[0]
                sample_transactions = preprocessed[preprocessed["customer_id"] == sample_customer]
                features = self.feature_engineer._engineer_customer_features(sample_transactions, sample_customer)
                validation_results["feature_engineering"] = {
                    "success": True,
                    "feature_count": len(features),
                }
            else:
                validation_results["feature_engineering"] = {
                    "success": False,
                    "error": "Insufficient transactions for feature engineering",
                }

            validation_results["overall"] = all(
                result.get("success", False) for result in validation_results.values() if isinstance(result, dict)
            )

            return validation_results

        except Exception as e:
            logger.error(f"Pipeline validation failed: {str(e)}")
            validation_results["overall"] = False
            validation_results["error"] = str(e)
            return validation_results
