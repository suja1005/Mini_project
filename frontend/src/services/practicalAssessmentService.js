import api from './api';

export const practicalAssessmentService = {
  async getStatus() {
    const response = await api.get('/practical-assessment/status');
    return response.data;
  },

  async start() {
    const response = await api.post('/practical-assessment/questions');
    return response.data;
  },

  async submit(assessmentId, answers) {
    const response = await api.post('/practical-assessment/submit', {
      assessment_id: assessmentId,
      answers
    });
    return response.data;
  },

  async getHistory() {
    const response = await api.get('/practical-assessment/history');
    return response.data;
  }
};
