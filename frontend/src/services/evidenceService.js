import api from './api';

export const evidenceService = {
  async getEvidence() {
    const response = await api.get('/evidence');
    return response.data;
  },

  async addProjectEvidence(projectData) {
    const response = await api.post('/evidence/project', projectData);
    return response.data;
  },

  async getSkillEvidence(skillName) {
    const response = await api.get(`/evidence/${encodeURIComponent(skillName)}`);
    return response.data;
  },

  async getVerifiedSkills() {
    const response = await api.get('/verified-skills');
    return response.data;
  },

  async recalculateEvidence() {
    const response = await api.post('/evidence/recalculate');
    return response.data;
  }
};
