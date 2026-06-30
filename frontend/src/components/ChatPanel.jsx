import { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "../api/client";
import SuggestedQuestions from "./SuggestedQuestions";

export default function ChatPanel() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dataTimestamp, setDataTimestamp] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  const handleSend = async (messageText) => {
    const text = messageText || input.trim();
    if (!text || loading) return;
    const updated = [...messages, { role: "user", content: text }];
    setMessages(updated); setInput(""); setLoading(true); setError(null);
    try {
      const result = await sendChatMessage(text, messages);
      setMessages([...updated, { role: "assistant", content: result.response }]);
      setDataTimestamp(result.data_timestamp);
    } catch { setError("Failed to get a response. Check the API connection."); }
    finally { setLoading(false); }
  };

  const onKey = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } };
  const fmt = (iso) => iso ? new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : null;

  return (
    <div className="flex flex-col h-[calc(100vh-13rem)] card overflow-hidden">
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-surface-border">
        <div>
          <h2 className="section-title">SupplyLens AI Analyst</h2>
          <p className="text-xs text-ink-muted">Grounded on live inventory & supplier data</p>
        </div>
        {dataTimestamp && (
          <span className="text-xs text-[#067647] bg-[#ecfdf3] border border-[#abefc6] px-2.5 py-1 rounded-full">● Data as of {fmt(dataTimestamp)}</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto chat-scroll px-5 py-4 space-y-4 bg-surface-sunken">
        {messages.length === 0 && <SuggestedQuestions onSelect={handleSend} />}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "assistant" && <div className="w-7 h-7 bg-brand-600 rounded-full flex items-center justify-center mr-2.5 mt-0.5 shrink-0 text-white text-xs font-semibold">AI</div>}
            <div className={`max-w-2xl px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${msg.role === "user" ? "bg-brand-600 text-white rounded-br-sm" : "bg-white border border-surface-border text-ink rounded-bl-sm"}`}>
              {msg.role === "assistant" ? <div className="ai-response" dangerouslySetInnerHTML={{ __html: fmtMd(msg.content) }} /> : msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="w-7 h-7 bg-brand-600 rounded-full flex items-center justify-center mr-2.5 shrink-0 text-white text-xs font-semibold">AI</div>
            <div className="bg-white border border-surface-border px-4 py-3 rounded-2xl rounded-bl-sm">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 bg-ink-muted rounded-full animate-bounce [animation-delay:0ms]" />
                <span className="w-2 h-2 bg-ink-muted rounded-full animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 bg-ink-muted rounded-full animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}
        {error && <div className="text-center text-[#b42318] text-sm bg-[#fef3f2] border border-[#fecdca] rounded-lg px-4 py-3">{error}</div>}
        <div ref={bottomRef} />
      </div>

      <div className="px-5 py-3.5 border-t border-surface-border bg-white">
        <div className="flex gap-3">
          <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKey} rows={2}
            placeholder="Ask about inventory risk, suppliers, or recommended actions..."
            className="flex-1 input resize-none" />
          <button onClick={() => handleSend()} disabled={!input.trim() || loading} className="btn-primary self-end disabled:opacity-40 disabled:cursor-not-allowed">Send</button>
        </div>
        <p className="text-xs text-ink-muted mt-2">Enter to send · Shift+Enter for new line</p>
      </div>
    </div>
  );
}

function fmtMd(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^• (.+)$/gm, "<li>$1</li>")
    .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>")
    .replace(/\n\n/g, "</p><p>").replace(/\n/g, "<br/>")
    .replace(/^/, "<p>").replace(/$/, "</p>");
}
