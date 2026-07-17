import axiosInstance from './axios';

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  created_at: string;
  updated_at: string;
}

export interface UpdateProfileRequest {
  full_name?: string;
  phone?: string;
}

export interface UpdatePasswordRequest {
  current_password: string;
  new_password: string;
}

export interface UserSettings {
  email_notifications: boolean;
  sms_notifications: boolean;
  language: string;
  dark_mode: boolean;
}

export const userApi = {
  async getProfile(): Promise<UserProfile> {
    const response = await axiosInstance.get<UserProfile>('/users/profile');
    return response.data;
  },

  async updateProfile(data: UpdateProfileRequest): Promise<UserProfile> {
    const response = await axiosInstance.put<UserProfile>('/users/profile', data);
    return response.data;
  },

  async updatePassword(data: UpdatePasswordRequest): Promise<void> {
    await axiosInstance.put('/users/password', data);
  },

  async getSettings(): Promise<UserSettings> {
    const response = await axiosInstance.get<UserSettings>('/users/settings');
    return response.data;
  },

  async updateSettings(data: Partial<UserSettings>): Promise<UserSettings> {
    const response = await axiosInstance.put<UserSettings>('/users/settings', data);
    return response.data;
  },

  async deleteAccount(): Promise<void> {
    await axiosInstance.delete('/users/account');
  },
};
