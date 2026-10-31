import api from './api';

export const roadmapService = {
  // ============================================================================
  // 3-Phase Adaptive Roadmap Endpoints
  // ============================================================================

  async getRoadmap() {
    const response = await api.get('/roadmap');
    return response.data;
  },

  async generateRoadmap(careerId = 'ai-engineer') {
    const response = await api.post('/roadmap/generate', { career_id: careerId });
    return response.data;
  },

  async getDashboard() {
    const response = await api.get('/roadmap/dashboard');
    return response.data;
  },

  async getProgress() {
    const response = await api.get('/roadmap/progress');
    return response.data;
  },

  // ============================================================================
  // Dashboard Summary & Recent Activity Endpoints
  // ============================================================================

  async getDashboardSummary() {
    const response = await api.get('/roadmap/dashboard/summary');
    return response.data;
  },

  async getRecentActivity() {
    const response = await api.get('/roadmap/dashboard/recent-activity');
    return response.data;
  },

  // ============================================================================
  // Topic Learning & Completion
  // ============================================================================

  async getTopicMaterials(phaseId, topicId) {
    const response = await api.get(`/roadmap/topics/${phaseId}/${topicId}`);
    return response.data;
  },

  async completeTopic(phaseId, topicId, practiceAnswer = null) {
    const response = await api.post(`/roadmap/topics/${phaseId}/${topicId}/complete`, {
      practice_answer: practiceAnswer
    });
    return response.data;
  },

  // ============================================================================
  // Phase Assessments
  // ============================================================================

  async generatePhaseAssessment(phaseId) {
    const response = await api.post(`/roadmap/phases/${phaseId}/assessment/generate`);
    return response.data;
  },

  async submitPhaseAssessment(phaseId, answers) {
    const response = await api.post(`/roadmap/phases/${phaseId}/assessment/submit`, { answers });
    return response.data;
  },

  async getPhaseAssessmentHistory(phaseId) {
    const response = await api.get(`/roadmap/phases/${phaseId}/assessment/history`);
    return response.data;
  },

  // ============================================================================
  // Legacy Methods – Preserved for Backward Compatibility
  // ============================================================================

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
  }
};
