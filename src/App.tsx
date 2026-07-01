import React, { useState, useRef, useEffect } from 'react';
import './App.css';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      sender: 'ai',
      text: "Welcome to the Intent-Driven Computational Engine. I only have core access to primitive add() and subtract() functions. Challenge me to calculate multiplication or division and watch me formulate an algorithm!"
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat to latest response messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessageText = input.trim();
    setInput('');
    
    // Append the user's chat bubble
    const userMsg: Message = { id: Date.now().toString(), sender: 'user', text: userMessageText };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userMessageText }),
      });
      
      const data = await response.json();
      
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: data.result || "Error processing strategy pipeline."
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { id: Date.now().toString(), sender: 'ai', text: "❌ Failed connecting to the local backend service engine. Make sure your FastAPI server is active!" }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>✨ Minimal Intent UI Calculator</h1>
        <p>Powered locally by Qwen-7B algorithmic reasoning primitives</p>
      </header>

      <div className="chat-window">
        <div className="messages-container">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-bubble ${msg.sender}`}>
              <div className="avatar">{msg.sender === 'user' ? '👤' : '🤖'}</div>
              <div className="message-text">
                {msg.sender === 'ai' ? (
                  <pre className="ai-reasoning-block">{msg.text}</pre>
                ) : (
                  msg.text
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-bubble ai loading">
              <div className="avatar">🤖</div>
              <div className="loading-dots">AI is formulating mathematical strategy...</div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your command (e.g., 'Multiply 6 by 4 step-by-step')..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            Send Intent
          </button>
        </form>
      </div>
    </div>
  );
}