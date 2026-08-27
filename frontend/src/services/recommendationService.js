import api from './api';

export const recommendationService = {
  async generateRecommendations() {
    const response = await api.post('/recommendations/generate');
    return response.data;
  },

  async getRecommendations() {
    const response = await api.get('/recommendations');
    return response.data;
  }
};
