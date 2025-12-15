import React from "react";

interface RAGChatbotProps {
  onClose?: () => void; // Optional, only for future use
}

const RAGChatbot: React.FC<RAGChatbotProps> = ({ onClose }) => {
  return (
    <div className="flex flex-col h-full bg-blue text-black rounded-xl overflow-hidden">
      {/* Static chat messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-2">
        <p>
          👋 Welcome! You can ask me anything about physical AI, books, or learning topics.
        </p>
        <p>
          I’m here to guide you, provide explanations, and assist with any questions.
        </p>
      </div>

      {/* Input Row (Disabled) */}
      <div className="border-t border-gray-200 p-3 flex gap-2">
        <input
          type="text"
          placeholder="Type your question..."
          className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium cursor-not-allowed"
          disabled
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default RAGChatbot;
