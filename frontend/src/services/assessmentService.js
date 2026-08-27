import api from './api';

export const assessmentService = {
  async getQuestions() {
    const response = await api.get('/assessment/questions');
    return response.data;
  },

  async submitAssessment(answers) {
    const response = await api.post('/assessment/submit', { answers });
    return response.data;
  },

  async getResults() {
    const response = await api.get('/assessment/results');
    return response.data;
  }
};
