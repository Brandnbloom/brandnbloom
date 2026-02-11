import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Avatar, AvatarFallback } from './ui/avatar';
import { toast } from 'sonner';
import { Send, LogOut, Sparkles, Brain, Zap, BarChart3 } from 'lucide-react';

const ChatPage = () => {
  const { user, token, logout, API } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        `${API}/chat`,
        {
          conversation_id: conversationId,
          message: input
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setConversationId(response.data.conversation_id);
      const aiMessage = {
        role: 'assistant',
        content: response.data.message,
        model_used: response.data.model_used,
        timestamp: new Date(response.data.timestamp)
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send message');
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const getModelIcon = (modelUsed) => {
    if (!modelUsed) return <Brain className="w-4 h-4" />;
    if (modelUsed.includes('openai')) return <Sparkles className="w-4 h-4 text-green-600" />;
    if (modelUsed.includes('anthropic')) return <Brain className="w-4 h-4 text-orange-600" />;
    if (modelUsed.includes('gemini')) return <Zap className="w-4 h-4 text-blue-600" />;
    return <Brain className="w-4 h-4" />;
  };

  const getModelName = (modelUsed) => {
    if (!modelUsed) return '';
    if (modelUsed.includes('openai')) return 'GPT-5.2';
    if (modelUsed.includes('anthropic')) return 'Claude Sonnet';
    if (modelUsed.includes('gemini')) return 'Gemini 3 Pro';
    return modelUsed;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 flex flex-col" data-testid="chat-page">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              🌸 Brand N Bloom
            </h1>
            <p className="text-sm text-gray-600">AI Co-Founder • Neural Router Active</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user?.business_name || user?.email}</p>
              <p className="text-xs text-gray-500">Business Owner</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={logout}
              data-testid="logout-button"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden flex flex-col max-w-5xl mx-auto w-full px-6 py-6">
        <ScrollArea className="flex-1 pr-4" data-testid="chat-messages">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 py-12">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                <Brain className="w-10 h-10 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome to Your AI Co-Founder</h2>
                <p className="text-gray-600 max-w-md">
                  I'm here to help you grow your business with intelligent insights and recommendations.
                  Ask me about marketing, customers, finance, HR, or operations.
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full max-w-2xl mt-8">
                <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer" onClick={() => setInput('How can I improve my marketing ROI?')}>
                  <p className="text-sm font-medium text-purple-600">💡 Marketing Strategy</p>
                  <p className="text-xs text-gray-500 mt-1">Optimize your campaigns</p>
                </Card>
                <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer" onClick={() => setInput('Analyze my customer churn risk')}>
                  <p className="text-sm font-medium text-pink-600">👥 Customer Insights</p>
                  <p className="text-xs text-gray-500 mt-1">Understand your customers</p>
                </Card>
                <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer" onClick={() => setInput('What are my biggest business risks?')}>
                  <p className="text-sm font-medium text-blue-600">⚠️ Risk Analysis</p>
                  <p className="text-xs text-gray-500 mt-1">Identify potential issues</p>
                </Card>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-4 ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                  data-testid={`message-${message.role}`}
                >
                  {message.role === 'assistant' && (
                    <Avatar className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500">
                      <AvatarFallback className="text-white">
                        {getModelIcon(message.model_used)}
                      </AvatarFallback>
                    </Avatar>
                  )}
                  <div
                    className={`max-w-2xl ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                        : 'bg-white border border-gray-200'
                    } rounded-2xl px-6 py-4 shadow-sm`}
                  >
                    {message.role === 'assistant' && message.model_used && (
                      <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                        {getModelIcon(message.model_used)}
                        <span>Powered by {getModelName(message.model_used)}</span>
                      </div>
                    )}
                    <p className={`text-sm whitespace-pre-wrap ${
                      message.role === 'user' ? 'text-white' : 'text-gray-800'
                    }`}>
                      {message.content}
                    </p>
                  </div>
                  {message.role === 'user' && (
                    <Avatar className="w-10 h-10 bg-gray-200">
                      <AvatarFallback className="text-gray-600">
                        {user?.business_name?.[0] || user?.email?.[0] || 'U'}
                      </AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
              {loading && (
                <div className="flex gap-4 justify-start">
                  <Avatar className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500">
                    <AvatarFallback className="text-white">
                      <Brain className="w-4 h-4 animate-pulse" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-white border border-gray-200 rounded-2xl px-6 py-4 shadow-sm">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </ScrollArea>

        {/* Input Area */}
        <div className="mt-6">
          <form onSubmit={sendMessage} className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask your AI Co-Founder anything..."
              disabled={loading}
              className="flex-1 h-12 text-base"
              data-testid="chat-input"
            />
            <Button
              type="submit"
              disabled={loading || !input.trim()}
              className="h-12 px-6 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
              data-testid="send-message-button"
            >
              <Send className="w-5 h-5" />
            </Button>
          </form>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Powered by Neural Router • Intelligently choosing between GPT-5.2, Claude Sonnet, and Gemini 3
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;