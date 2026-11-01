import api from './api';

export const careerService = {
  async getCareers() {
    const response = await api.get('/careers');
    return response.data;
  },

  async getCareerById(careerId) {
    const response = await api.get(`/careers/${careerId}`);
    return response.data;
  },

  async getCareerAnalysis(careerId) {
    const response = await api.get(`/career-analysis/${careerId}`);
    return response.data;
  },

  async selectCareer(careerId) {
    const response = await api.post(`/career-selection/${careerId}`);
    return response.data;
  }
};
