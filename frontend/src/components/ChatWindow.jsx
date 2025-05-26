
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

export default function ChatWindow() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);

  // Load from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('chatHistory');
    if (stored) setHistory(JSON.parse(stored));
  }, []);

  // Save to localStorage whenever history updates
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(history));
  }, [history]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedHistory = [...history, userMessage];
    setHistory(updatedHistory);

    try {
      const res = await axios.post('http://localhost:5000/ask', { question: input });
      const botMessage = { role: 'bot', content: res.data.answer };
      setHistory([...updatedHistory, botMessage]);
      setInput('');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="bg-white rounded shadow p-4">
      <div className="h-64 overflow-y-auto mb-4 border p-2 bg-gray-50">
        {history.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block px-3 py-1 rounded ${msg.role === 'user' ? 'bg-blue-100' : 'bg-green-100'}`}>
              {msg.role === 'bot' ? <ReactMarkdown>{msg.content}</ReactMarkdown> : msg.content}
            </span>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border px-3 py-2 rounded"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your question..."
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}
