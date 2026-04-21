import { FormEvent, KeyboardEvent, useEffect, useMemo, useRef, useState } from "react";

type Role = "user" | "assistant";

type ChatMessage = {
  role: Role;
  content: string;
};

type AgentStateSummary = {
  intent: string;
  name: string;
  email: string;
  platform: string;
  lead_stage: string;
  lead_captured: boolean;
};

type ChatResponse = {
  session_id: string;
  response: string;
  state: AgentStateSummary;
};

const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") ||
  "http://127.0.0.1:8010";

const START_MESSAGE =
  "Hi! I’m the AutoStream AI Agent. Ask me about pricing, features, refund policy, or start signup.";

const QUICK_PROMPTS = [
  "Hi, tell me about your pricing.",
  "What features come with the Pro plan?",
  "I want to try Pro for my YouTube channel.",
  "What is your refund policy?",
];

function emptyAgentState(): AgentStateSummary {
  return {
    intent: "",
    name: "",
    email: "",
    platform: "",
    lead_stage: "",
    lead_captured: false,
  };
}

export function AgentConsole() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: START_MESSAGE },
  ]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [agentState, setAgentState] = useState<AgentStateSummary>(emptyAgentState());
  const [sessionId, setSessionId] = useState<string | null>(null);

  const messageEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    setSessionId(window.localStorage.getItem("autostream_session_id"));
  }, []);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  const canSend = useMemo(() => message.trim().length > 0 && !loading, [message, loading]);

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) {
      return;
    }

    setLoading(true);
    setError("");
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmed,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = (await response.json()) as ChatResponse;

      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
        if (typeof window !== "undefined") {
          window.localStorage.setItem("autostream_session_id", data.session_id);
        }
      }

      setAgentState(data.state ?? emptyAgentState());
      setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
    } catch {
      const fallback =
        "I couldn't reach the backend API. Please run uvicorn on port 8010 and try again.";
      setError(fallback);
      setMessages((prev) => [...prev, { role: "assistant", content: fallback }]);
    } finally {
      setLoading(false);
    }
  }

  async function resetChat() {
    if (sessionId) {
      try {
        await fetch(`${API_BASE}/api/reset`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ session_id: sessionId }),
        });
      } catch {
        // Keep local reset even if backend reset fails.
      }
    }

    setMessages([{ role: "assistant", content: START_MESSAGE }]);
    setAgentState(emptyAgentState());
    setMessage("");
    setError("");
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSend) {
      return;
    }
    void send(message);
  }

  function onMessageKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (!canSend) {
        return;
      }
      void send(message);
    }
  }

  return (
    <div className="grid xl:grid-cols-[1.2fr_0.8fr] gap-6 md:gap-8">
      <div className="rounded-3xl border border-border bg-card/70 backdrop-blur-lg p-5 md:p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-primary mb-2">
              Live Agent
            </p>
            <h3 className="font-display text-4xl md:text-5xl">Chat Console</h3>
          </div>
          <button
            type="button"
            onClick={() => {
              void resetChat();
            }}
            className="font-mono text-[10px] uppercase tracking-widest px-3 py-2 rounded-full border border-border hover:border-primary hover:text-primary transition"
          >
            Reset
          </button>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {QUICK_PROMPTS.map((prompt) => (
            <button
              key={prompt}
              type="button"
              onClick={() => {
                void send(prompt);
              }}
              disabled={loading}
              className="rounded-full border border-border px-3 py-1.5 text-xs font-mono hover:border-primary hover:text-primary transition disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>

        <div className="h-[430px] md:h-[500px] overflow-y-auto rounded-2xl border border-border bg-background/50 p-4 space-y-4">
          {messages.map((item, index) => (
            <div
              key={`${item.role}-${index}`}
              className={item.role === "user" ? "flex justify-end" : "flex justify-start"}
            >
              <div
                className={
                  "max-w-[90%] rounded-2xl p-4 whitespace-pre-wrap " +
                  (item.role === "user"
                    ? "bg-secondary border border-border"
                    : "bg-primary/10 border border-primary/35")
                }
              >
                <div className="font-mono text-[10px] uppercase tracking-[0.2em] opacity-70 mb-1">
                  {item.role === "user" ? "You" : "Agent"}
                </div>
                <p className="text-sm md:text-base leading-relaxed">{item.content}</p>
              </div>
            </div>
          ))}

          {loading ? (
            <div className="font-mono text-xs uppercase tracking-widest text-primary">
              Agent is thinking...
            </div>
          ) : null}

          <div ref={messageEndRef} />
        </div>

        <form onSubmit={onSubmit} className="mt-4 flex flex-col gap-3">
          <textarea
            rows={3}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={onMessageKeyDown}
            placeholder="Type your message and press Enter"
            className="w-full rounded-2xl border border-border bg-background/70 px-4 py-3 outline-none resize-none focus:border-primary transition"
          />
          <div className="flex items-center justify-between gap-3">
            <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              API: {API_BASE}/api/chat
            </p>
            <button
              type="submit"
              disabled={!canSend}
              className="bg-primary text-primary-foreground font-display text-xl px-6 py-3 rounded-full hover:opacity-90 disabled:opacity-50 transition"
            >
              Send →
            </button>
          </div>
        </form>

        {error ? <p className="mt-3 text-sm text-red-300">{error}</p> : null}
      </div>

      <div className="rounded-3xl border border-border bg-card/45 backdrop-blur-lg p-5 md:p-6">
        <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-primary mb-3">Session State</p>
        <h3 className="font-display text-4xl md:text-5xl mb-6">Memory</h3>

        <div className="space-y-3">
          <StateRow label="Intent" value={agentState.intent || "Not detected"} />
          <StateRow label="Lead Stage" value={agentState.lead_stage || "Not started"} />
          <StateRow label="Name" value={agentState.name || "Not provided"} />
          <StateRow label="Email" value={agentState.email || "Not provided"} />
          <StateRow label="Platform" value={agentState.platform || "Not provided"} />
          <StateRow
            label="Lead"
            value={agentState.lead_captured ? "Captured ✅" : "Not captured"}
          />
        </div>

        <div className="mt-8 rounded-2xl border border-primary/40 bg-primary/10 p-4">
          <p className="font-mono text-[10px] uppercase tracking-widest text-primary mb-2">Guardrail</p>
          <p className="text-sm text-muted-foreground">
            Lead tool executes only after collecting <span className="text-foreground">name</span>, <span className="text-foreground">email</span>, and <span className="text-foreground">platform</span>.
          </p>
        </div>
      </div>
    </div>
  );
}

function StateRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-border bg-background/40 px-4 py-3 flex items-center justify-between gap-3">
      <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">{label}</span>
      <span className="text-sm md:text-base text-right">{value}</span>
    </div>
  );
}
