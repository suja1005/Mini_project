import api from './api';

export const roadmapService = {
  async generateRoadmap(careerId = 'ai-engineer') {
    const response = await api.post('/roadmap/generate', { career_id: careerId });
    return response.data;
  },

  async getRoadmap() {
    const response = await api.get('/roadmap');
    return response.data;
  },

  async getTaskDetail(taskId) {
    const response = await api.get(`/roadmap/tasks/${taskId}`);
    return response.data;
  },

  async startTask(taskId) {
    const response = await api.post(`/roadmap/tasks/${taskId}/start`);
    return response.data;
  },

  async toggleSubtopic(taskId, topicId, subtopicId, completed) {
    const response = await api.post(`/roadmap/tasks/${taskId}/topics/toggle`, {
      topic_id: topicId,
      subtopic_id: subtopicId,
      completed
    });
    return response.data;
  },

  async completeLearning(taskId) {
    const response = await api.post(`/roadmap/tasks/${taskId}/complete-learning`);
    return response.data;
  },

  async generateQuestions(taskId) {
    const response = await api.post(`/roadmap/tasks/${taskId}/generate-questions`);
    return response.data;
  },

  async submitVerification(taskId, answers) {
    const response = await api.post(`/roadmap/tasks/${taskId}/submit-verification`, { answers });
    return response.data;
  },

  async getVerificationHistory(taskId) {
    const response = await api.get(`/roadmap/tasks/${taskId}/verification-history`);
    return response.data;
  },

  async getProgress() {
    const response = await api.get('/roadmap/progress');
    return response.data;
  }
};
