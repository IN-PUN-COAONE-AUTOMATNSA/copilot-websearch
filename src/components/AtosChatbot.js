import React from 'react';
import { Bot } from 'lucide-react';

const AtosChatbot = () => {
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

      {/* Copilot Studio Embedded Chat */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        <div className="flex-1 p-4">
          <div className="h-full bg-white rounded-lg shadow-lg overflow-hidden border border-blue-200">
            <iframe 
              src="https://copilotstudio.microsoft.com/environments/a2af0bff-c97e-e451-9151-19167c6f5252/bots/git_atosWebSearchCopilot/webchat?__version__=2" 
              frameBorder="0" 
              style={{ width: '100%', height: '100%' }}
              title="Atos AI Assistant - Copilot Studio"
              allowFullScreen
            />
          </div>
        </div>
        
        {/* Footer */}
        <div className="p-4 bg-white border-t border-blue-200">
          <div className="text-center text-xs text-gray-500">
            Powered by Atos AI • Web Search Enhanced • 
            <span className="text-blue-600 font-medium"> Always Learning</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AtosChatbot;
