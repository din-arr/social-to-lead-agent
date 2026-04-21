import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { HeroScene, RobotScene } from "@/components/Scene3D";
import { AgentConsole } from "@/components/AgentConsole";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => ({
    meta: [
      { title: "AutoStream — Agentic Video Editing for Creators" },
      {
        name: "description",
        content:
          "AutoStream turns social conversations into qualified leads with a LangGraph-powered agent. RAG knowledge, intent detection, tool calling — built for creators.",
      },
      { property: "og:title", content: "AutoStream — Agentic Video Editing" },
      {
        property: "og:description",
        content:
          "An agentic workflow that listens, qualifies, and converts. Built on LangGraph + RAG.",
      },
    ],
  }),
});

const features = [
  {
    n: "01",
    title: "Intent Detection",
    body: "Classifies every message into casual, inquiry, or high-intent — before a single token is wasted.",
  },
  {
    n: "02",
    title: "RAG Knowledge",
    body: "Local JSON knowledge base. Pricing, policies, features — answered with receipts, not hallucinations.",
  },
  {
    n: "03",
    title: "Tool Calling",
    body: "Mock lead-capture fires only when name, email and platform are confirmed. Never premature.",
  },
  {
    n: "04",
    title: "Stateful Memory",
    body: "LangGraph state buffers 5–6 turns so the agent never forgets the channel you mentioned.",
  },
];

const plans = [
  {
    name: "Basic",
    price: "$29",
    pop: false,
    perks: ["10 videos / month", "720p resolution", "Email support"],
  },
  {
    name: "Pro",
    price: "$79",
    pop: true,
    perks: ["Unlimited videos", "4K resolution", "AI captions", "24/7 support"],
  },
];

function Index() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      {/* NAV */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-background/40 border-b border-border">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10 h-16 flex items-center justify-between">
          <a href="/" className="font-display text-2xl tracking-tighter">
            auto<span className="text-primary">/</span>stream
          </a>
          <nav className="hidden md:flex gap-8 font-mono text-xs uppercase tracking-widest">
            <a href="#agent" className="hover:text-primary transition">Agent</a>
            <a href="#flow" className="hover:text-primary transition">Flow</a>
            <a href="#live-agent" className="hover:text-primary transition">Live</a>
            <a href="#pricing" className="hover:text-primary transition">Pricing</a>
            <a href="#stack" className="hover:text-primary transition">Stack</a>
          </nav>
          <a
            href="#live-agent"
            className="font-mono text-xs uppercase tracking-widest bg-primary text-primary-foreground px-4 py-2 rounded-full hover:bg-primary/90 transition"
          >
            Try the agent →
          </a>
        </div>
      </header>

      {/* HERO */}
      <section className="relative min-h-screen pt-24 pb-24 md:pb-32 grain-overlay">
        <div className="absolute inset-0 -z-10" style={{ background: "var(--gradient-noir)" }} />
        <div className="absolute inset-0 z-0">
          <HeroScene />
        </div>

        <div className="relative z-10 pointer-events-none mx-auto max-w-[1600px] px-6 md:px-10 pt-16 md:pt-24">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, ease: "easeOut" }}
            className="font-mono text-xs uppercase tracking-[0.3em] text-primary mb-6"
          >
            ↳ Social-to-Lead · Agentic Workflow · v1.0
          </motion.div>

          <h1 className="font-display text-mega leading-[0.82]">
            <motion.span
              initial={{ opacity: 0, y: 80 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.1 }}
              className="block"
            >
              AGENTS
            </motion.span>
            <motion.span
              initial={{ opacity: 0, y: 80 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.25 }}
              className="block text-stroke"
            >
              THAT CLOSE.
            </motion.span>
            <motion.span
              initial={{ opacity: 0, y: 80 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.4 }}
              className="block text-primary"
            >
              NOT CHAT.
            </motion.span>
          </h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7, duration: 0.8 }}
            className="mt-10 max-w-xl text-lg md:text-xl text-muted-foreground"
          >
            AutoStream is a conversational AI agent for creators. It detects intent, retrieves
            knowledge with RAG, and calls real tools — turning Instagram DMs into qualified leads.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.6 }}
            className="mt-10 flex flex-wrap gap-4 pointer-events-auto"
          >
            <a
              href="#live-agent"
              className="inline-flex items-center gap-2 bg-primary text-primary-foreground font-display text-lg px-7 py-4 rounded-full hover:translate-y-[-2px] transition shadow-[0_10px_40px_-10px_oklch(0.89_0.21_125_/_0.6)]"
            >
              Start chatting →
            </a>
            <a
              href="#pricing"
              className="inline-flex items-center gap-2 border border-border font-display text-lg px-7 py-4 rounded-full hover:bg-secondary transition"
            >
              View pricing
            </a>
          </motion.div>
        </div>

        {/* marquee at bottom */}
        <div className="absolute bottom-0 left-0 right-0 border-y border-border bg-background/60 backdrop-blur-sm py-4 overflow-hidden">
          <div className="marquee flex gap-12 whitespace-nowrap font-display text-3xl">
            {Array.from({ length: 2 }).map((_, k) => (
              <div key={k} className="flex gap-12 shrink-0">
                {["LANGGRAPH", "★", "RAG-NATIVE", "★", "TOOL-CALLING", "★", "STATEFUL", "★", "GPT-4o-mini", "★", "CLAUDE 3", "★", "GEMINI 1.5", "★"].map((t, i) => (
                  <span key={i} className={i % 2 === 0 ? "text-foreground" : "text-primary"}>
                    {t}
                  </span>
                ))}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AGENT SECTION with Robot */}
      <section id="agent" className="relative py-24 md:py-40 border-t border-border">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10 grid md:grid-cols-2 gap-16 items-center">
          <div>
            <div className="font-mono text-xs uppercase tracking-[0.3em] text-primary mb-6">
              ↳ 01 / The Agent
            </div>
            <h2 className="font-display text-huge mb-8">
              NOT A<br />
              <span className="text-primary">CHATBOT.</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-md mb-8">
              Inflx agents are designed to do the four things bots can&apos;t — understand intent,
              answer with sources, qualify in real time, and trigger real backend actions.
            </p>
            <div className="flex flex-wrap gap-2 font-mono text-xs">
              {["intent.classify()", "rag.retrieve()", "state.buffer()", "tools.call()"].map((t) => (
                <span key={t} className="px-3 py-1.5 bg-secondary rounded-full border border-border">
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className="h-[500px] md:h-[600px] relative">
            <div
              className="absolute inset-0 rounded-3xl"
              style={{ background: "radial-gradient(circle at 50% 50%, oklch(0.89 0.21 125 / 0.15), transparent 60%)" }}
            />
            <RobotScene />
          </div>
        </div>
      </section>

      {/* FEATURES GRID */}
      <section id="flow" className="relative py-24 md:py-40 border-t border-border bg-secondary/30">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10">
          <div className="flex items-end justify-between flex-wrap gap-6 mb-16">
            <h2 className="font-display text-huge max-w-3xl">
              FOUR MOVES.<br />ZERO HALLUCINATION.
            </h2>
            <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground max-w-xs">
              Each capability is independently testable, observable, and replaceable.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-px bg-border border border-border rounded-3xl overflow-hidden">
            {features.map((f) => (
              <motion.div
                key={f.n}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-80px" }}
                transition={{ duration: 0.6 }}
                className="bg-background p-8 md:p-12 group hover:bg-card transition"
              >
                <div className="flex items-baseline gap-6 mb-6">
                  <span className="font-mono text-sm text-primary">{f.n}</span>
                  <span className="h-px flex-1 bg-border" />
                </div>
                <h3 className="font-display text-4xl md:text-5xl mb-4 group-hover:text-primary transition">
                  {f.title}
                </h3>
                <p className="text-muted-foreground text-base">{f.body}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CONVERSATION FLOW */}
      <section className="relative py-24 md:py-40 border-t border-border">
        <div className="mx-auto max-w-[1400px] px-6 md:px-10">
          <div className="font-mono text-xs uppercase tracking-[0.3em] text-primary mb-6">
            ↳ Live conversation trace
          </div>
          <h2 className="font-display text-huge mb-16">DM → DEAL.<br />IN 5 TURNS.</h2>

          <div className="space-y-6 max-w-4xl">
            {[
              { who: "user", text: "Hi, tell me about your pricing." },
              { who: "agent", tag: "intent: inquiry · rag.retrieve(pricing)", text: "We have two plans — Basic at $29/mo (10 videos, 720p) and Pro at $79/mo (unlimited, 4K, AI captions)." },
              { who: "user", text: "That sounds good, I want to try Pro for my YouTube channel." },
              { who: "agent", tag: "intent: HIGH · qualify()", text: "Amazing — let&apos;s get you set up. What&apos;s your name and email?" },
              { who: "user", text: "Aanya Mehta, aanya@channelhq.io" },
              { who: "agent", tag: "tools.mock_lead_capture(✓)", text: "Lead captured. Welcome to Pro, Aanya — our team will email your YouTube onboarding shortly." },
            ].map((m, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: m.who === "user" ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.05 }}
                className={m.who === "user" ? "flex justify-end" : "flex justify-start"}
              >
                <div
                  className={
                    "max-w-2xl rounded-2xl p-5 " +
                    (m.who === "user"
                      ? "bg-secondary border border-border"
                      : "bg-primary/10 border border-primary/40")
                  }
                >
                  <div className="font-mono text-[10px] uppercase tracking-widest mb-2 opacity-70">
                    {m.who === "user" ? "USER" : "AGENT"}
                    {m.tag ? <span className="text-primary ml-2">// {m.tag}</span> : null}
                  </div>
                  <p className="text-base md:text-lg" dangerouslySetInnerHTML={{ __html: m.text }} />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* LIVE AGENT */}
      <section id="live-agent" className="relative py-24 md:py-32 border-t border-border bg-secondary/20">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10">
          <div className="font-mono text-xs uppercase tracking-[0.3em] text-primary mb-6">
            ↳ Runtime console
          </div>
          <h2 className="font-display text-huge mb-8">
            CHAT WITH<br />
            <span className="text-primary">THE AGENT.</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-3xl mb-10">
            This console is directly connected to your LangGraph backend workflow
            for intent detection, RAG retrieval, and lead-capture tool execution.
          </p>
          <AgentConsole />
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing" className="relative py-24 md:py-40 border-t border-border bg-secondary/30">
        <div className="mx-auto max-w-[1400px] px-6 md:px-10">
          <h2 className="font-display text-huge mb-16">
            PICK A<br />
            <span className="text-primary">PLAN.</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {plans.map((p) => (
              <motion.div
                key={p.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className={
                  "relative p-10 rounded-3xl border-2 " +
                  (p.pop
                    ? "bg-primary text-primary-foreground border-primary shadow-[var(--shadow-glow)]"
                    : "bg-card border-border")
                }
              >
                {p.pop && (
                  <span className="absolute -top-3 right-8 bg-foreground text-background font-mono text-[10px] uppercase tracking-widest px-3 py-1 rounded-full">
                    Most popular
                  </span>
                )}
                <div className="font-display text-5xl mb-2">{p.name}</div>
                <div className="font-display text-7xl mb-8">
                  {p.price}
                  <span className="text-2xl opacity-60">/mo</span>
                </div>
                <ul className="space-y-3 mb-8">
                  {p.perks.map((perk) => (
                    <li key={perk} className="flex items-center gap-3 text-lg">
                      <span className={p.pop ? "text-primary-foreground" : "text-primary"}>✦</span>
                      {perk}
                    </li>
                  ))}
                </ul>
                <a
                  href="#live-agent"
                  className={
                    "inline-block w-full text-center font-display text-lg py-4 rounded-full transition " +
                    (p.pop
                      ? "bg-primary-foreground text-primary hover:opacity-90"
                      : "bg-primary text-primary-foreground hover:opacity-90")
                  }
                >
                  Choose {p.name}
                </a>
              </motion.div>
            ))}
          </div>
          <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground mt-8">
            ↳ No refunds after 7 days · 24/7 support included on Pro plan
          </p>
        </div>
      </section>

      {/* STACK */}
      <section id="stack" className="relative py-24 md:py-40 border-t border-border">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10 grid md:grid-cols-3 gap-12">
          <div className="md:col-span-1">
            <div className="font-mono text-xs uppercase tracking-[0.3em] text-primary mb-6">
              ↳ Mandatory stack
            </div>
            <h2 className="font-display text-6xl md:text-7xl">BUILT ON<br />SHARP TOOLS.</h2>
          </div>
          <div className="md:col-span-2 grid sm:grid-cols-2 gap-4 font-mono text-sm">
            {[
              ["LANG", "LangGraph for stateful agents"],
              ["LLM", "GPT-4o-mini · Gemini 1.5 · Claude 3"],
              ["RAG", "Local JSON knowledge base"],
              ["MEM", "5–6 turn buffer, persisted"],
              ["TOOL", "mock_lead_capture(name,email,platform)"],
              ["DEPLOY", "WhatsApp via Meta webhooks"],
            ].map(([k, v]) => (
              <div key={k} className="border border-border rounded-2xl p-6 hover:border-primary transition">
                <div className="text-primary text-xs mb-2">{k}</div>
                <div className="text-foreground text-base">{v}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-24 md:py-32 border-t border-border overflow-hidden">
        <div
          className="absolute inset-0"
          style={{ background: "radial-gradient(ellipse at center, oklch(0.89 0.21 125 / 0.15), transparent 70%)" }}
        />
        <div className="relative mx-auto max-w-[1600px] px-6 md:px-10 text-center">
          <h2 className="font-display text-mega">
            <span className="block">SHIP THE</span>
            <span className="block text-primary float-y">AGENT.</span>
          </h2>
          <p className="text-xl text-muted-foreground mt-8 max-w-xl mx-auto">
            Stop scripting flows. Start shipping conversations that close.
          </p>
          <a
            href="#live-agent"
            className="inline-block mt-12 bg-primary text-primary-foreground font-display text-2xl px-10 py-6 rounded-full hover:scale-105 transition"
          >
            Open live chat →
          </a>
        </div>
      </section>

      <footer className="border-t border-border py-10">
        <div className="mx-auto max-w-[1600px] px-6 md:px-10 flex flex-wrap items-center justify-between gap-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
          <div>© 2026 AutoStream · Built with LangGraph</div>
          <div>Inflx by ServiceHive</div>
        </div>
      </footer>
    </div>
  );
}
