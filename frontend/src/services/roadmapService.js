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

  async getTasks() {
    const response = await api.get('/roadmap/tasks');
    return response.data;
  },

  async updateTaskStatus(taskId, status) {
    const response = await api.put(`/roadmap/tasks/${taskId}`, { status });
    return response.data;
  },

  async completeTask(taskId) {
    const response = await api.post(`/roadmap/tasks/${taskId}/complete`);
    return response.data;
  }
};
