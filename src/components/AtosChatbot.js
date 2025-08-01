import React, { useState, useRef, useEffect } from 'react';
import { Send, Search, Bot, User } from 'lucide-react';

const AtosChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m your Atos AI Assistant. I can help you search the web and answer your questions. What would you like to know today?',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // TODO: Replace with your actual Copilot Studio Agent API endpoint
      const API_ENDPOINT = process.env.REACT_APP_COPILOT_API_ENDPOINT || 'YOUR_COPILOT_STUDIO_ENDPOINT_HERE';
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any required headers for Copilot Studio API
          // 'Authorization': `Bearer ${process.env.REACT_APP_API_KEY}`,
          // 'Ocp-Apim-Subscription-Key': process.env.REACT_APP_SUBSCRIPTION_KEY,
        },
        body: JSON.stringify({
          message: currentInput,
          // Add other required parameters for Copilot Studio
          sessionId: `session-${Date.now()}`, // Generate or maintain session ID
          // userId: 'user-id', // If required
          // channelId: 'web-chat', // If required
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      // Extract response content - adjust based on Copilot Studio response format
      const botResponse = data.message || data.response || data.content || 'I apologize, but I received an unexpected response format.';

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: botResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('API Error:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `I apologize, but I'm currently experiencing technical difficulties. Please try again later.\n\nError: ${error.message}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-lg">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Atos AI Assistant</h1>
            <p className="text-blue-100 text-sm">Powered by Web Search & AI</p>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div className={`p-2 rounded-full ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white shadow-md text-blue-600'
              }`}>
                {message.type === 'user' ? (
                  <User className="w-5 h-5" />
                ) : (
                  <Bot className="w-5 h-5" />
                )}
              </div>

              {/* Message Bubble */}
              <div className={`max-w-3xl ${
                message.type === 'user' ? 'text-right' : 'text-left'
              }`}>
                <div className={`inline-block p-4 rounded-2xl shadow-sm ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-md'
                    : 'bg-white text-gray-800 rounded-tl-md border border-blue-100'
                }`}>
                  <div className="whitespace-pre-wrap">{message.content}</div>
                </div>
                <div className={`text-xs text-gray-500 mt-1 ${
                  message.type === 'user' ? 'text-right' : 'text-left'
                }`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-white shadow-md text-blue-600">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-white p-4 rounded-2xl rounded-tl-md shadow-sm border border-blue-100">
                <div className="flex items-center gap-2">
                  <Search className="w-4 h-4 text-blue-600 animate-spin" />
                  <span className="text-gray-600">Searching and analyzing...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-blue-200">
          <div className="flex gap-3 items-end">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything... I'll search the web and provide you with comprehensive answers."
                className="w-full p-4 pr-12 border border-blue-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[60px] max-h-32"
                rows={1}
                style={{ 
                  height: 'auto',
                  minHeight: '60px'
                }}
                onInput={(e) => {
                  e.target.style.height = 'auto';
                  e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
                }}
                disabled={isLoading}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 text-white p-4 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-md"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          {/* Footer */}
          <div className="text-center mt-3 text-xs text-gray-500">
            Powered by Atos AI • Web Search Enhanced • 
            <span className="text-blue-600 font-medium"> Always Learning</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AtosChatbot;