"use client";
import React, { useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const apiURL = "http://localhost:80";

  // Send user queries
  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch(`${apiURL}/query?q=${encodeURIComponent(input)}`, {
        method: "POST",
      });
      const data = await res.json();
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant" as const, content: data.response || "No response." },
      ]);
    } catch {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "Error contacting API." },
      ]);
    }
    setLoading(false);
  };

  // Handle button actions like reset, load documents, evaluate
  const handleAction = async (endpoint: string) => {
    setLoading(true);
    try {
      const res = await fetch(`${apiURL}/${endpoint}`, { method: "POST" });
      const data = await res.json();
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant" as const, content: data.response || "No response" },
      ]);
    } catch {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant" as const, content: `Failed to ${endpoint}.` },
      ]);
    }
    setLoading(false);
  };

  // Clear the chat
  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-8">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-10 flex flex-col min-h-[700px]">
        <h1 className="text-3xl font-bold mb-2 text-center">sRAG Chat</h1>
        <p className="text-gray-500 mb-6 text-center">
          Exploring secure RAG
        </p>
        <div className="flex gap-4 mb-6 justify-center flex-wrap">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
            onClick={() => handleAction("reset")}
            disabled={loading}
          >
            Reset DB
          </button>
          <button
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
            onClick={() =>
              handleAction("add_documents")
            }
            disabled={loading}
          >
            Load Documents
          </button>
          <button
            className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition"
            onClick={() =>
              handleAction("evaluate")
            }
            disabled={loading}
          >
            Evaluate
          </button>
          <button
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition"
            onClick={handleClearChat}
            disabled={loading || messages.length === 0}
          >
            Clear Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto mb-6 border rounded-xl p-6 bg-gray-50 h-[500px]">
          {messages.length === 0 && (
            <div className="text-gray-400 text-center mt-16 text-lg">Start the conversation…</div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`mb-4 flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`px-5 py-3 rounded-lg max-w-2xl text-lg ${
                  msg.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-gray-900"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-gray-400 text-center">Loading...</div>
          )}
        </div>
        <div className="flex gap-3">
          <input
            className="flex-1 border rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring"
            type="text"
            placeholder="Type your question…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            disabled={loading}
          />
          <button
            className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700 transition"
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}