import api from './api';

export const progressService = {
  async getProgress() {
    const response = await api.get('/progress');
    return response.data;
  },

  async getSkillProgress() {
    const response = await api.get('/progress/skills');
    return response.data;
  },

  async getEmployabilityProgress() {
    const response = await api.get('/progress/employability');
    return response.data;
  },

  async getHistory() {
    const response = await api.get('/progress/history');
    return response.data;
  }
};
