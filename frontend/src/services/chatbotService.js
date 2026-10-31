import api from './api';

export const chatbotService = {
  async sendMessage(message, history = []) {
    const response = await api.post('/chatbot/message', {
      message,
      history
    });
    return response.data;
  }
};
