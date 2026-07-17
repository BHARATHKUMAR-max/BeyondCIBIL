import axiosInstance from './axios';

export interface PredictionRequest {
  customer_id: string;
  savings_ratio: number;
  average_monthly_income: number;
  income_consistency: number;
  total_expense: number;
  transaction_frequency: number;
}

export interface PredictionResponse {
  customer_id: string;
  alternative_credit_score: number;
  repayment_probability: number;
  risk_category: string;
  confidence: number;
  prediction: string;
  top_positive_factors: Array<{
    feature: string;
    contribution: number;
    impact: string;
  }>;
  top_negative_factors: Array<{
    feature: string;
    contribution: number;
    impact: string;
  }>;
  recommendations: string[];
  model_version: string;
  prediction_timestamp: string;
}

export interface BankConnectionRequest {
  phone_number: string;
  bank_name: string;
}

export interface BankConnectionResponse {
  customer: {
    customer_id: string;
    phone_number: string;
    bank_name: string;
    account_number: string;
    account_type: string;
    account_balance: number;
    monthly_income: number;
    total_expense: number;
    savings: number;
    emis: Array<{
      loan_type: string;
      amount: number;
      remaining_tenure: number;
      interest_rate: number;
    }>;
    recurring_payments: Array<{
      name: string;
      amount: number;
      frequency: string;
    }>;
  };
  transaction_summary: {
    total_transactions: number;
    total_debit: number;
    total_credit: number;
    average_monthly_debit: number;
    average_monthly_credit: number;
    category_spending: Record<string, number>;
    spending_categories: string[];
    top_spending_category: string;
  };
  alternative_credit_score: number;
  repayment_probability: number;
  confidence: number;
  risk_category: string;
  shap_explanation: Record<string, any>;
  recommendations: string[];
}

export const predictionApi = {
  async predict(data: PredictionRequest): Promise<PredictionResponse> {
    const response = await axiosInstance.post<PredictionResponse>(
      '/api/v1/predictions/credit-score',
      data
    );
    return response.data;
  },

  async predictFromBank(data: BankConnectionRequest): Promise<BankConnectionResponse> {
    const response = await axiosInstance.post<BankConnectionResponse>(
      '/api/v1/predictions/predict-from-bank',
      data
    );
    return response.data;
  },

  async batchPredict(data: PredictionRequest[]): Promise<{
    predictions: PredictionResponse[];
    total_count: number;
    success_count: number;
    failure_count: number;
    errors: Array<{ index: number; error: string }>;
  }> {
    const response = await axiosInstance.post('/predictions/batch', {
      predictions: data,
    });
    return response.data;
  },

  async getHealth(): Promise<{
    status: string;
    model_version: string;
    model_loaded: boolean;
    scaler_loaded: boolean;
    feature_columns_loaded: boolean;
    shap_explainer_loaded: boolean;
    required_features: string[];
    feature_count: number;
  }> {
    const response = await axiosInstance.get('/predictions/health');
    return response.data;
  },

  async getMetrics(): Promise<{
    pipeline_name: string;
    version: string;
    model_version: string;
    target_latency_ms: number;
    feature_count: number;
    supports_batch: boolean;
    supports_shap: boolean;
    supports_recommendations: boolean;
  }> {
    const response = await axiosInstance.get('/predictions/metrics');
    return response.data;
  },
};
