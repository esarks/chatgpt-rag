// src/App.jsx
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [files, setFiles] = useState([]);
  const [uploadStatuses, setUploadStatuses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const savedHistory = localStorage.getItem("chatHistory");
    if (savedHistory) {
      setChatHistory(JSON.parse(savedHistory));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");
    setSources([]);

    const response = await fetch("http://localhost:5000/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let result = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      result += chunk;
      setAnswer(prev => prev + chunk);
    }

    setLoading(false);

    const meta = await fetch("http://localhost:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    }).then(res => res.json());

    const sourcesFromMeta = meta.sources || [];
    setSources(sourcesFromMeta);

    setChatHistory(prev => [
      ...prev,
      { question, answer: result, sources: sourcesFromMeta }
    ]);

    setQuestion("");
    setAnswer("");
  };

  const handleFileUpload = async () => {
    if (!files || files.length === 0) return;

    const statuses = files.map(file => ({ name: file.name, status: "Uploading..." }));
    setUploadStatuses(statuses);

    for (let i = 0; i < files.length; i++) {
      const formData = new FormData();
      formData.append("file", files[i]);
      try {
        const res = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData
        });
        const text = await res.text();
        console.log("Response text:", text);
        let result;
        try {
          result = JSON.parse(text);
        } catch {
          result = { error: "Invalid JSON returned from server." };
        }
        const updatedStatus = result.message
          ? `✅ ${result.filename} (${result.chunks} chunks)`
          : `❌ ${result.error || "Unknown error"}`;
        statuses[i].status = updatedStatus;
        setUploadStatuses([...statuses]);
      } catch (err) {
        statuses[i].status = `❌ ${err.message}`;
        setUploadStatuses([...statuses]);
      }
    }
  };

  return (
    <div className={darkMode ? "min-h-screen bg-gray-900 text-white p-4" : "min-h-screen bg-gray-50 text-gray-800 p-4"}>
      <div className="max-w-2xl mx-auto space-y-4">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">📚 Pinecone RAG Chatbot</h1>
          <div className="flex gap-2 items-center">
            <button
              onClick={() => {
                setChatHistory([]);
                localStorage.removeItem("chatHistory");
              }}
              className="text-sm border px-3 py-1 rounded hover:bg-red-100 hover:text-red-600"
            >Clear History</button>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="text-sm border px-3 py-1 rounded"
            >{darkMode ? 'Light Mode' : 'Dark Mode'}</button>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex gap-2">
            <input
              type="file"
              multiple
              onChange={e => setFiles(Array.from(e.target.files))}
              className="flex-1 border p-2 rounded"
            />
            <button
              onClick={handleFileUpload}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >Upload</button>
          </div>

          {uploadStatuses.length > 0 && (
            <ul className="text-sm space-y-1">
              {uploadStatuses.map((file, idx) => (
                <li key={idx} className="flex justify-between items-center border rounded px-2 py-1 bg-white text-gray-800">
                  <span className="truncate mr-2">{file.name}</span>
                  <span className="text-xs font-mono">{file.status}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="flex flex-col gap-2 border rounded px-3 py-2 bg-white shadow-sm focus-within:ring-2 focus-within:ring-blue-500">
          <textarea
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            className="w-full outline-none bg-transparent text-base resize-none h-24 leading-relaxed"
          />
          <div className="flex justify-end">
            <button
              onClick={handleAsk}
              disabled={loading}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
            >Ask</button>
          </div>
        </div>

        {chatHistory.map((item, idx) => (
          <div key={idx} className={darkMode ? "border border-gray-700 p-4 rounded bg-gray-800" : "border p-4 rounded bg-white"}>
            <p className="text-sm text-gray-500">Q: {item.question}</p>
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={darkMode ? oneDark : oneLight}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                }
              }}
            >
              {item.answer}
            </ReactMarkdown>
            {item.sources.length > 0 && (
              <p className="text-xs text-gray-400 mt-2">Sources: {item.sources.join(", ")}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
