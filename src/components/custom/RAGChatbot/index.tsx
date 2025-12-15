import React, { useState, useEffect, useCallback } from 'react';
import ChatUI from './ChatUI';
import { ChatMessage } from './types'; // Import ChatMessage from centralized types

interface RAGChatbotProps {
  onClose?: () => void; // Add onClose prop here
}

const RAGChatbot: React.FC<RAGChatbotProps> = ({ onClose }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = useCallback(async (query: string, mode: string, selectedText?: string) => {
    const userMessage: ChatMessage = { type: 'user', text: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setLoading(true);

    try {
      const payload = {
        query,
        mode,
        ...(selectedText && { selected_text: selectedText }),
      };

      const response = await fetch('http://localhost:8000/api/v1/chat', { // Assuming backend runs on 8000
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage: ChatMessage = {
        type: 'bot',
        text: data.answer,
        sources: data.sources,
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: 'bot', text: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial welcome message
  useEffect(() => {
    setMessages([{ type: 'bot', text: 'Hello! How can I help you with the book today?' }]);
  }, []);

  return (
    <div className="flex-grow flex flex-col h-[calc(100%-4rem)]">
      <ChatUI
        onSendMessage={sendMessage}
        messages={messages}
        loading={loading}
        onClose={onClose}
      />
    </div>
  );
};

export default RAGChatbot;
