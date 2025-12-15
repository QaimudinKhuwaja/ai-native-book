import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './types'; // Import ChatMessage from centralized types

interface ChatUIProps {
  onSendMessage: (query: string, mode: string, selectedText?: string) => void;
  messages: ChatMessage[];
  loading: boolean;
  onClose?: () => void; // Optional prop for closing the chat
}

const ChatUI: React.FC<ChatUIProps> = ({ onSendMessage, messages, loading, onClose }) => {
  const [inputText, setInputText] = useState('');
  const [chatMode, setChatMode] = useState('global-book'); // 'global-book' or 'selected-text-only'
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(e.target.value);
  };

  const handleModeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setChatMode(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim()) {
      let selectedText: string | undefined = undefined;
      if (chatMode === 'selected-text-only') {
        selectedText = window.getSelection()?.toString() || '';
        if (!selectedText) {
          alert('Please select some text to use "selected-text-only" mode.');
          return;
        }
      }
      onSendMessage(inputText, chatMode, selectedText);
      setInputText('');
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Messages Container */}
      <div className="flex-grow overflow-y-auto p-4 space-y-3 max-h-[calc(100%-140px)]">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg ${
              msg.type === 'user'
                ? 'ml-auto bg-primary-500 text-white max-w-[90%] sm:max-w-[85%]'
                : 'mr-auto bg-white/10 backdrop-blur-sm text-gray-100 border border-white/10 max-w-[90%] sm:max-w-[85%]'
            }`}
          >
            <div className="font-medium mb-1">
              {msg.type === 'user' ? 'You' : 'AI Assistant'}:
            </div>
            <div className="text-sm whitespace-pre-wrap">{msg.text}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-2 pt-2 border-t border-white/20 text-xs">
                <div className="font-medium mb-1">Sources:</div>
                <ul className="space-y-1">
                  {msg.sources.map((source, srcIndex) => (
                    <li key={srcIndex} className="truncate">
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-300 hover:text-blue-200 underline truncate"
                      >
                        {source.page_title}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="mr-auto p-3 rounded-lg bg-white/10 backdrop-blur-sm text-gray-100 border border-white/10 max-w-[90%] sm:max-w-[85%]">
            <div className="font-medium mb-1">AI Assistant:</div>
            <div className="text-sm">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-white/10 flex-shrink-0">
        <form onSubmit={handleSubmit} className="space-y-3">
          <select
            value={chatMode}
            onChange={handleModeChange}
            className="w-full px-3 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-300 appearance-none bg-[length:1rem] bg-no-repeat bg-[right_0.5rem_center] pr-8"
          >
            <option value="global-book" className="bg-gray-800 text-white">Global Book</option>
            <option value="selected-text-only" className="bg-gray-800 text-white">Selected Text Only</option>
          </select>

          <div className="flex gap-2">
            <input
              type="text"
              value={inputText}
              onChange={handleInputChange}
              placeholder="Ask a question..."
              className="flex-grow px-3 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-300"
              disabled={loading}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="submit"
              className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-300 disabled:opacity-50 flex items-center justify-center"
              disabled={loading}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatUI;