import React from "react";
import { Home, MessageCircle } from "lucide-react";

const HOME_URL = import.meta.env.VITE_HOME_URL || "http://localhost:5173";
const CHATBOT_URL = import.meta.env.VITE_CHATBOT_URL || "http://localhost:5174";
export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 px-6 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        <div className="flex items-center gap-2">
          <span className="text-xl font-bold text-blue-600">
            AI Shop Assistant
          </span>
        </div>

        <div className="flex items-center gap-4">
          <a
            href={HOME_URL}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
          >
            <Home size={18} />
            <span>Home</span>
          </a>

          <a
            href={CHATBOT_URL}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-md transition-all"
          >
            <MessageCircle size={18} />
            <span>chatbot</span>
          </a>
        </div>
      </div>
    </nav>
  );
};