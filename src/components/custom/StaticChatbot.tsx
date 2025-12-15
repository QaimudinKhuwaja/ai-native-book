import React, { useState, useRef, useEffect } from 'react';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const StaticChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { text: 'Ask anything about Physical AI', sender: 'bot' },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const chatboxRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleToggleChat = () => setIsOpen(!isOpen);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage: Message = { text: inputValue, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    // Simulate bot typing
    setIsTyping(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { text: 'This book is about Physical Ai.', sender: 'bot' },
      ]);
      setIsTyping(false);
    }, 1000); // 1-second typing effect
  };

  useEffect(() => {
    if (isOpen && inputRef.current) inputRef.current.focus();
  }, [isOpen]);

  useEffect(() => {
    if (chatboxRef.current) {
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <div className="fixed right-5 bottom-5 z-50 flex flex-col items-end space-y-4">
      {/* Chatbox */}
      <div
        className={`w-80 sm:w-96 h-96 sm:h-[480px] flex flex-col rounded-xl shadow-2xl transition-all duration-300 ease-in-out ${
          isOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
        } bg-gray-900 text-white`}
      >
        {/* Header */}
        <div className="bg-blue-900 text-white p-4 rounded-t-xl flex justify-between items-center">
          <h3 className="font-bold text-lg">AI Assistant</h3>
        </div>

        {/* Messages */}
        <div
          ref={chatboxRef}
          className="flex-1 p-4 overflow-y-auto flex flex-col space-y-3 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-800"
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`max-w-[80%] p-3 rounded-lg break-words ${
                msg.sender === 'user'
                  ? 'self-end bg-blue-800 text-white'
                  : 'self-start bg-gray-800 text-white'
              }`}
            >
              {msg.text}
            </div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <div className="self-start bg-gray-800 text-white p-3 rounded-lg max-w-[40%]">
              <span className="animate-pulse">Typing...</span>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-3 border-t border-gray-700 flex items-center space-x-2">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            placeholder="Type your message..."
            className="flex-1 resize-none rounded-lg p-2 bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-700"
            rows={1}
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-900 hover:bg-blue-800 text-white px-5 py-2 rounded-lg font-semibold transition-colors"
          >
            Send
          </button>
        </div>
      </div>

      {/* Floating Chat Icon */}
      <button
        onClick={handleToggleChat}
        className="w-16 h-16 bg-black rounded-full flex items-center justify-center text-3xl text-white shadow-lg hover:scale-110 transition-transform"
      >
        Chat💬
      </button>
    </div>
  );
};

export default StaticChatbot;
