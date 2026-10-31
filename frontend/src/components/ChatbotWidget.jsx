import React, { useState, useRef, useEffect } from 'react';
import { chatbotService } from '../services/chatbotService';
import { 
  Bot, 
  X, 
  Send, 
  Sparkles, 
  Loader2, 
  User, 
  MessageSquare, 
  HelpCircle,
  Lightbulb,
  Code2,
  ChevronDown,
  RefreshCw
} from 'lucide-react';

const SUGGESTED_QUESTIONS = [
  "Explain this topic in simple English",
  "Give me a Python example",
  "What should I study next?",
  "How can I improve my assessment score?",
  "Suggest a project for my current learning phase",
  "Explain the difference between AI and Machine Learning"
];

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'model',
      content: "Hello! I am your **AI Career Assistant**. I track your career roadmap, completed topics, and assessment progress to guide your learning journey. How can I help you today?"
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen, messages]);

  const handleSendMessage = async (textToSend = null) => {
    const text = (textToSend || inputMessage).trim();
    if (!text || loading) return;

    const userMsg = { role: 'user', content: text };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInputMessage('');
    setError(null);
    setLoading(true);

    try {
      // Map history format for backend
      const apiHistory = newHistory.slice(-6).map(m => ({
        role: m.role === 'model' ? 'model' : 'user',
        content: m.content
      }));

      const res = await chatbotService.sendMessage(text, apiHistory);
      setMessages(prev => [
        ...prev,
        { role: 'model', content: res.reply }
      ]);
    } catch (err) {
      console.error("Chatbot API error:", err);
      setError("Unable to connect with AI Assistant right now. Please check your backend connection or try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderFormattedText = (content) => {
    // Simple parser for code blocks and bold text
    const parts = content.split(/(```[\s\S]*?```)/g);
    return parts.map((part, idx) => {
      if (part.startsWith('```') && part.endsWith('```')) {
        const lines = part.slice(3, -3).trim().split('\n');
        const lang = lines[0].match(/^[a-z]+/i) ? lines[0] : '';
        const code = lang ? lines.slice(1).join('\n') : lines.join('\n');
        return (
          <div key={idx} className="my-2 p-3 bg-slate-900 text-emerald-300 rounded-lg text-xs font-mono overflow-x-auto border border-slate-700">
            {lang && <div className="text-[10px] text-slate-400 mb-1 uppercase font-semibold">{lang}</div>}
            <pre className="whitespace-pre-wrap">{code}</pre>
          </div>
        );
      }

      // Format bold text **text**
      const boldParts = part.split(/(\*\*.*?\*\*)/g);
      return (
        <span key={idx}>
          {boldParts.map((bPart, bIdx) => {
            if (bPart.startsWith('**') && bPart.endsWith('**')) {
              return <strong key={bIdx} className="font-semibold text-slate-900 dark:text-white">{bPart.slice(2, -2)}</strong>;
            }
            return bPart;
          })}
        </span>
      );
    });
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Floating Chat Icon (Initial View) */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="group relative flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-indigo-300 dark:focus:ring-indigo-800"
          aria-label="Open AI Career Assistant"
        >
          <Bot className="w-7 h-7 transition-transform group-hover:rotate-12" />
          <span className="absolute -top-1 -right-1 flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500 border-2 border-white dark:border-slate-900"></span>
          </span>
          <span className="absolute -top-9 right-0 bg-slate-900 text-white text-[11px] font-medium py-1 px-2.5 rounded-md opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap shadow-md">
            AI Career Assistant
          </span>
        </button>
      )}

      {/* Floating Chat Panel */}
      {isOpen && (
        <div className="flex flex-col w-[360px] sm:w-[420px] h-[580px] max-h-[85vh] bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-200">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-white/10 rounded-xl backdrop-blur-sm">
                <Bot className="w-5 h-5 text-indigo-100" />
              </div>
              <div>
                <h3 className="text-sm font-bold flex items-center space-x-1.5 leading-tight">
                  <span>AI Career Assistant</span>
                  <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                </h3>
                <p className="text-[11px] text-indigo-200 flex items-center space-x-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  <span>Personalized Roadmap Guide</span>
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 rounded-lg text-indigo-200 hover:text-white hover:bg-white/10 transition-colors focus:outline-none"
              aria-label="Close Chat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50/50 dark:bg-slate-950/40 text-xs">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex items-start space-x-2.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role !== 'user' && (
                  <div className="w-7 h-7 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
                <div
                  className={`max-w-[82%] px-3.5 py-2.5 rounded-2xl leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-none shadow-sm'
                      : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200/80 dark:border-slate-700/60 rounded-bl-none shadow-sm'
                  }`}
                >
                  {renderFormattedText(msg.content)}
                </div>
                {msg.role === 'user' && (
                  <div className="w-7 h-7 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center space-x-2 text-slate-400 text-xs py-1">
                <Loader2 className="w-4 h-4 animate-spin text-indigo-500" />
                <span className="italic">AI Assistant is analyzing your roadmap context...</span>
              </div>
            )}

            {error && (
              <div className="p-2.5 rounded-lg bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-xs">
                {error}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Prompt Chips */}
          <div className="px-3 py-2 bg-slate-100/70 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex items-center space-x-1.5 overflow-x-auto no-scrollbar">
            <Lightbulb className="w-3.5 h-3.5 text-amber-500 shrink-0 ml-1" />
            {SUGGESTED_QUESTIONS.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(q)}
                disabled={loading}
                className="shrink-0 px-2.5 py-1 text-[11px] rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-indigo-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition-colors disabled:opacity-50"
              >
                {q}
              </button>
            ))}
          </div>

          {/* Input Bar */}
          <div className="p-3 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex items-center space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              placeholder="Ask anything about topics, code, or career..."
              className="flex-1 px-3.5 py-2 text-xs rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={loading || !inputMessage.trim()}
              className="p-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 active:scale-95 disabled:opacity-40 disabled:hover:bg-indigo-600 transition-all focus:outline-none"
              aria-label="Send Message"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotWidget;
