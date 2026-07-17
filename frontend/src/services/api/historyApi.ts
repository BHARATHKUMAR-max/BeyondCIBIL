import axiosInstance from './axios';

export interface PredictionHistoryItem {
  id: string;
  customer_id: string;
  alternative_credit_score: number;
  repayment_probability: number;
  risk_category: string;
  confidence: number;
  prediction_timestamp: string;
  model_version: string;
}

export const historyApi = {
  async getHistory(limit: number = 50, offset: number = 0): Promise<{
    predictions: PredictionHistoryItem[];
    total_count: number;
    limit: number;
    offset: number;
  }> {
    const response = await axiosInstance.get('/predictions/history', {
      params: { limit, offset },
    });
    return response.data;
  },

  async getPredictionById(id: string): Promise<PredictionHistoryItem> {
    const response = await axiosInstance.get(`/predictions/history/${id}`);
    return response.data;
  },

  async deletePrediction(id: string): Promise<void> {
    await axiosInstance.delete(`/predictions/history/${id}`);
  },
};
