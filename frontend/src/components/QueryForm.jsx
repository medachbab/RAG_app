import React, { useState, useRef, useEffect } from "react";
import { ragQuery } from "../api";

export default function QueryForm() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(3);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError("Please enter a question.");
      return;
    }

    // Add user message to chat
    const userMessage = { 
      type: 'user', 
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setChatHistory(prev => [...prev, userMessage]);

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await ragQuery(query, parseInt(topK || 3));
      setResult(res);
      
      // Add bot response to chat
      const botMessage = { 
        type: 'bot', 
        content: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: res.sources
      };
      setChatHistory(prev => [...prev, botMessage]);
      setQuery(""); // Clear input after successful response
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.error || err.message || "Query failed";
      setError(errorMsg);
      
      // Add error to chat
      const errorMessage = { 
        type: 'error', 
        content: `Error: ${errorMsg}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setChatHistory([]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="h-full flex flex-col bg-white/80 text-gray-800">
      {/* Chat Header */}
      <div className="p-6 border-b border-gray-200 flex items-center justify-between bg-white/80">
        <div className="flex items-center gap-3">
          <div>
            <h3 className="text-lg font-semibold">Product Assistant</h3>
          </div>
        </div>
        <button
          onClick={clearChat}
          className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-sm text-white flex items-center gap-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          Clear Chat
        </button>
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 max-h-[500px]">
        {chatHistory.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-20 h-20 mx-auto rounded-full bg-gradient-to-r from-blue-100 to-blue-200 flex items-center justify-center mb-4 text-blue-700">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
              </svg>

            </div>
            <h4 className="text-xl font-medium mb-2">Start a Conversation</h4>
            <p className="text-gray-600 max-w-md mx-auto">
              Ask any question about our products. I'll search through documentation and provide accurate answers with sources.
            </p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 ${
                  msg.type === 'user'
                    ? 'bg-gradient-to-r from-blue-100 to-blue-50 text-blue-800 border border-blue-200'
                    : msg.type === 'error'
                    ? 'bg-red-50 text-red-700 border border-red-100'
                    : 'bg-white text-gray-800 border border-gray-200'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  {msg.type === 'bot' && (
                    <div className="w-6 h-6 rounded-full bg-gradient-to-r from-green-500 to-blue-500 flex items-center justify-center">
                      <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                      </svg>
                    </div>
                  )}
                  <span className="text-xs text-gray-500">
                    {msg.type === 'user' ? 'You' : msg.type === 'bot' ? 'Assistant' : 'System'} • {msg.timestamp}
                  </span>
                </div>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                
                {/* Sources for bot messages */}
                {msg.type === 'bot' && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-gray-700/50">
                    <div className="flex items-center gap-2 mb-3">
                      <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                      </svg>
                      <span className="text-sm font-medium text-gray-700">Sources ({msg.sources.length})</span>
                    </div>
                    <div className="grid grid-cols-1 gap-2">
                      {msg.sources.map((src, i) => (
                        <div
                          key={i}
                          className="p-3 rounded-lg bg-white border border-gray-200"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs px-2 py-1 rounded-full bg-blue-500/20 text-blue-300">
                              Source {i + 1}
                            </span>
                            {src.distance && (
                              <span className="text-xs text-gray-500">
                                Confidence: {(1 - src.distance).toFixed(2)}
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-700 leading-relaxed">
                            {src.source.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        
        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-2xl p-4 bg-white border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150"></div>
                </div>
                <span className="text-sm text-gray-600">Searching product database...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-gray-200 bg-white/80">
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-100">
              <p className="text-sm text-red-700 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {error}
              </p>
            </div>
          )}

          <div className="flex items-end gap-4">
            <div className="flex-1">
              <div className="relative">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask about product features, specifications, or comparisons..."
                  rows={2}
                  className="w-full rounded-xl border border-gray-200 bg-white text-gray-800 placeholder-gray-400 p-4 pr-12 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  disabled={loading}
                />
                <div className="absolute right-3 bottom-3">
                  <button
                    type="submit"
                    disabled={loading || !query.trim()}
                    className="p-2 rounded-lg bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                  >
                    {loading ? (
                      <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>
            
            <div className="flex-shrink-0">
              <div className="bg-gray-100 rounded-lg p-3">
                <label className="text-xs text-gray-600 block mb-1">RETRIEVAL COUNT</label>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setTopK(Math.max(1, topK - 1))}
                    className="w-7 h-7 rounded-md bg-white border border-gray-200 hover:bg-gray-50 flex items-center justify-center"
                    disabled={topK <= 1}
                  >
                    <span className="text-sm">−</span>
                  </button>
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={topK}
                    onChange={(e) => setTopK(Math.min(10, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="w-12 text-center bg-transparent border-0 text-gray-800"
                  />
                  <button
                    type="button"
                    onClick={() => setTopK(Math.min(10, topK + 1))}
                    className="w-7 h-7 rounded-md bg-white border border-gray-200 hover:bg-gray-50 flex items-center justify-center"
                    disabled={topK >= 10}
                  >
                    <span className="text-sm">+</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}