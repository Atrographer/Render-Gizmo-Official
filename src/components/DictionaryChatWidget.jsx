import React, { useState, useRef, useEffect } from 'react';

export default function DictionaryChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const STORAGE_KEY = "dictionary_chatbot_history";
  const API_URL = "https://render-gizmo-official.onrender.com/api/chat";

  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch (e) {}
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { text: input.trim(), sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input.trim();
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput }),
      });

      if (!response.ok) throw new Error('Server error');

      const data = await response.json();
      setMessages(prev => [...prev, { text: data.response, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        text: 'Connection failed. The server may be waking up (30-60s). Please try again.',
        sender: 'bot'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChatHistory = () => {
    if (window.confirm("Clear all lookup history?")) {
      localStorage.removeItem(STORAGE_KEY);
      setMessages([]);
    }
  };

  return (
    <div style={{ position: 'fixed', bottom: '20px', right: '25px', zIndex: 99999, fontFamily: 'sans-serif' }}>
      
      <button 
        onClick={() => setIsOpen(!isOpen)}
        style={{ 
          width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#2563eb', color: 'white', 
          fontSize: '24px', border: 'none', cursor: 'pointer', boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {isOpen && (
        <div style={{ 
          position: 'absolute', bottom: '80px', right: '0', width: '360px', height: '480px', 
          backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 8px 24px rgba(0,0,0,0.15)', 
          display: 'flex', flexDirection: 'column', overflow: 'hidden' 
        }}>
          
          <div style={{ backgroundColor: '#2563eb', color: 'white', padding: '16px', fontWeight: 'bold', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>GIZMO Dictionary Assistant</span>
            {messages.length > 0 && (
              <button onClick={clearChatHistory} style={{ background: 'transparent', border: 'none', color: '#bfdbfe', fontSize: '12px', textDecoration: 'underline', cursor: 'pointer' }}>
                Clear
              </button>
            )}
          </div>
          
          <div style={{ flex: '1', padding: '16px', overflowY: 'auto', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {messages.length === 0 && (
              <div style={{ alignSelf: 'flex-start', backgroundColor: '#e2e8f0', color: '#1e293b', padding: '10px 14px', borderRadius: '14px', fontSize: '14px' }}>
                Hello! Ask me for any word (e.g. tau, gizmo, deterministic)
              </div>
            )}

            {messages.map((msg, index) => (
              <div 
                key={index}
                style={{ 
                  alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: msg.sender === 'user' ? '#2563eb' : '#e2e8f0',
                  color: msg.sender === 'user' ? 'white' : '#1e293b',
                  padding: '10px 14px',
                  borderRadius: '14px',
                  borderBottomRightRadius: msg.sender === 'user' ? '2px' : '14px',
                  borderBottomLeftRadius: msg.sender === 'bot' ? '2px' : '14px',
                  maxWidth: '75%',
                  fontSize: '14px',
                  whiteSpace: 'pre-line'
                }}
              >
                {msg.text}
              </div>
            ))}

            {isLoading && (
              <div style={{ alignSelf: 'flex-start', backgroundColor: '#e2e8f0', color: '#64748b', padding: '10px 14px', borderRadius: '14px', fontSize: '13px' }}>
                Searching GIZMO dictionary...<br />
                <span style={{ fontSize: '11px' }}>(May take 30-60s on cold start)</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSend} style={{ display: 'flex', padding: '12px', borderTop: '1px solid #e2e8f0', gap: '8px', backgroundColor: 'white' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a word..."
              style={{ flex: 1, padding: '10px 14px', borderRadius: '9999px', border: '1px solid #cbd5e1', outline: 'none' }}
              disabled={isLoading}
            />
            <button 
              type="submit"
              style={{ 
                backgroundColor: isLoading ? '#93c5fd' : '#2563eb', 
                color: 'white', 
                border: 'none', 
                padding: '0 20px', 
                borderRadius: '9999px', 
                cursor: isLoading ? 'not-allowed' : 'pointer' 
              }}
              disabled={isLoading}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
