"use client";

import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  Cpu,
  Download,
  FileText,
  Gauge,
  Layers,
  Loader2,
  Network,
  Radar as RadarIcon,
  ShieldCheck,
  Sparkles,
  Zap,
} from "lucide-react";
import {
  Bar,
  BarChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type AnalyzeResponse = {
  report: string;
  risk_score: {
    overall_risk_level?: string;
    overall_score?: number;
    likelihood_score?: number;
    impact_score?: number;
    executive_decision?: string;
    scoring_rationale?: string;
    top_risk_categories?: string[];
  };
  function_scores: Record<string, number>;
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001";

const scenarios = [
  {
    title: "Financial AI Chatbot",
    label: "Finance",
    text: "Assess the AI risks of deploying a customer-facing AI chatbot for a global financial services company that provides investment guidance, processes transactions, integrates with internal banking APIs, and handles sensitive customer data.",
  },
  {
    title: "Healthcare Copilot",
    label: "Healthcare",
    text: "Assess the AI risks of deploying a generative AI copilot for a multinational healthcare organization that assists doctors with diagnosis recommendations, patient summarization, and treatment planning across multiple hospitals while integrating with electronic health record systems and third-party APIs.",
  },
  {
    title: "AI Hiring Assistant",
    label: "HR",
    text: "Assess the AI risks of deploying an AI hiring assistant that screens resumes, ranks candidates, and recommends hiring decisions for a large enterprise operating across multiple regions.",
  },
];

const agents = [
  ["GOVERN", "Governance and accountability", ShieldCheck],
  ["MAP", "Context and stakeholder impact", Network],
  ["MEASURE", "Testing and monitoring", Gauge],
  ["MANAGE", "Mitigation and residual risk", Activity],
  ["PLAYBOOK", "NIST implementation guidance", Layers],
  ["SCORE", "LLM-based scoring", Brain],
] as const;

export default function Home() {
  const [scenario, setScenario] = useState(scenarios[0].text);
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState<"dashboard" | "report" | "architecture">(
    "dashboard"
  );
  const [error, setError] = useState<string | null>(null);

  async function runAnalysis() {
    setLoading(true);
    setError(null);
    setData(null);
    setView("dashboard");

    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario }),
      });

      if (!res.ok) throw new Error(`Analyze failed: ${res.status}`);

      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setLoading(false);
    }
  }

  async function downloadPdf() {
    try {
      const res = await fetch(`${API_BASE}/export-pdf`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario }),
      });

      if (!res.ok) throw new Error("PDF export failed.");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "ai_risk_advisory_report.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "PDF export failed.");
    }
  }

  const chartData = useMemo(() => {
    if (!data) return [];
    return Object.entries(data.function_scores || {}).map(([name, score]) => ({
      name,
      score,
    }));
  }, [data]);

  const sections = useMemo(() => parseReport(data?.report || ""), [data]);

  const risk = data?.risk_score;
  const overallLevel = risk?.overall_risk_level || "Not analyzed";
  const overallScore = risk?.overall_score ?? 0;
  const likelihood = risk?.likelihood_score ?? 0;
  const impact = risk?.impact_score ?? 0;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.18),transparent_35%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.10),transparent_30%),linear-gradient(135deg,#020617,#0f172a)]" />

      <div className="mx-auto max-w-7xl px-4 py-6 md:px-8">
        <Header />

        <section className="mt-6 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <ScenarioPanel
            scenario={scenario}
            setScenario={setScenario}
            loading={loading}
            runAnalysis={runAnalysis}
            downloadPdf={downloadPdf}
            dataReady={!!data}
          />

          <SystemPanel loading={loading} completed={!!data} />
        </section>

        {error && (
          <div className="mt-6 rounded-2xl border border-red-400/30 bg-red-500/10 p-4 text-red-200">
            {error}
          </div>
        )}

        <section className="mt-6">
          <Tabs view={view} setView={setView} />
        </section>

        {view === "dashboard" && (
          <Dashboard
            data={data}
            chartData={chartData}
            overallLevel={overallLevel}
            overallScore={overallScore}
            likelihood={likelihood}
            impact={impact}
            loading={loading}
          />
        )}

        {view === "report" && <Report sections={sections} raw={data?.report || ""} />}

        {view === "architecture" && <Architecture />}
      </div>
    </main>
  );
}

function Header() {
  return (
    <section className="rounded-3xl border border-emerald-400/20 bg-slate-900/70 p-6 shadow-2xl shadow-emerald-500/10 backdrop-blur md:p-8">
      <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
        <div>
          <div className="mb-4 flex flex-wrap gap-2">
            {["Azure OpenAI", "Azure AI Search", "Key Vault", "FastAPI", "NIST AI RMF"].map(
              (item) => (
                <span
                  key={item}
                  className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs font-black uppercase tracking-wide text-emerald-300"
                >
                  {item}
                </span>
              )
            )}
          </div>

          <h1 className="max-w-5xl text-4xl font-black tracking-tight text-white md:text-6xl">
            AI Risk Advisor
          </h1>

          <p className="mt-4 max-w-3xl text-base leading-7 text-slate-300 md:text-lg">
            A full-stack Azure AI governance platform for assessing high-risk AI
            deployments using NIST AI RMF, multi-agent orchestration, risk scoring,
            and executive reporting.
          </p>
        </div>

        <div className="rounded-3xl border border-emerald-400/20 bg-slate-950 p-5">
          <div className="flex items-center gap-2 text-sm font-black uppercase tracking-[0.2em] text-emerald-300">
            <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_16px_#34d399]" />
            System Online
          </div>
          <p className="mt-3 text-sm text-slate-400">
            React frontend connected to FastAPI backend.
          </p>
        </div>
      </div>
    </section>
  );
}

function ScenarioPanel({
  scenario,
  setScenario,
  loading,
  runAnalysis,
  downloadPdf,
  dataReady,
}: {
  scenario: string;
  setScenario: (value: string) => void;
  loading: boolean;
  runAnalysis: () => void;
  downloadPdf: () => void;
  dataReady: boolean;
}) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Sparkles className="h-6 w-6 text-emerald-300" />
        <h2 className="text-2xl font-black">Scenario Console</h2>
      </div>

      <div className="mb-4 grid gap-3 md:grid-cols-3">
        {scenarios.map((item) => (
          <button
            key={item.title}
            onClick={() => setScenario(item.text)}
            className="rounded-2xl border border-slate-700 bg-slate-950 p-4 text-left transition hover:border-emerald-400/50 hover:bg-emerald-400/10"
          >
            <span className="rounded-full bg-emerald-400/10 px-2 py-1 text-xs font-black text-emerald-300">
              {item.label}
            </span>
            <p className="mt-3 font-black text-white">{item.title}</p>
            <p className="mt-2 line-clamp-3 text-xs leading-5 text-slate-400">
              {item.text}
            </p>
          </button>
        ))}
      </div>

      <textarea
        value={scenario}
        onChange={(e) => setScenario(e.target.value)}
        className="h-44 w-full resize-none rounded-2xl border border-slate-700 bg-slate-950 p-4 text-sm leading-6 text-slate-100 outline-none transition focus:border-emerald-400"
      />

      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <button
          onClick={runAnalysis}
          disabled={loading}
          className="flex items-center justify-center gap-2 rounded-2xl bg-emerald-400 px-5 py-4 font-black text-slate-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Running Analysis
            </>
          ) : (
            <>
              <Zap className="h-5 w-5" />
              Generate Report
            </>
          )}
        </button>

        <button
          onClick={downloadPdf}
          disabled={!dataReady || loading}
          className="flex items-center justify-center gap-2 rounded-2xl border border-emerald-400/30 bg-slate-950 px-5 py-4 font-black text-emerald-300 transition hover:bg-emerald-400 hover:text-slate-950 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <Download className="h-5 w-5" />
          Download PDF
        </button>
      </div>
    </section>
  );
}

function SystemPanel({
  loading,
  completed,
}: {
  loading: boolean;
  completed: boolean;
}) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black">Agent Pipeline</h2>
          <p className="mt-1 text-sm text-slate-400">Execution workflow</p>
        </div>
        {loading ? (
          <Loader2 className="h-6 w-6 animate-spin text-emerald-300" />
        ) : completed ? (
          <CheckCircle2 className="h-6 w-6 text-emerald-300" />
        ) : (
          <Cpu className="h-6 w-6 text-slate-500" />
        )}
      </div>

      <div className="space-y-3">
        {agents.map(([name, detail, Icon], index) => (
          <motion.div
            key={name}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.04 }}
            className={`rounded-2xl border p-4 ${
              completed
                ? "border-emerald-400/30 bg-emerald-400/10"
                : loading
                ? "border-emerald-400/20 bg-slate-950"
                : "border-slate-700 bg-slate-950"
            }`}
          >
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-slate-900 p-2 text-emerald-300">
                <Icon className="h-5 w-5" />
              </div>
              <div>
                <p className="font-black">{name}</p>
                <p className="text-xs text-slate-400">{detail}</p>
              </div>
              <div className="ml-auto">
                {completed ? (
                  <CheckCircle2 className="h-5 w-5 text-emerald-300" />
                ) : loading ? (
                  <span className="block h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-400" />
                ) : (
                  <span className="block h-2.5 w-2.5 rounded-full bg-slate-700" />
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

function Tabs({
  view,
  setView,
}: {
  view: string;
  setView: (value: "dashboard" | "report" | "architecture") => void;
}) {
  const tabs = [
    ["dashboard", "Dashboard", Activity],
    ["report", "Report", FileText],
    ["architecture", "Architecture", Cpu],
  ] as const;

  return (
    <div className="flex flex-wrap gap-3 rounded-3xl border border-slate-800 bg-slate-900/80 p-3">
      {tabs.map(([key, label, Icon]) => (
        <button
          key={key}
          onClick={() => setView(key)}
          className={`flex items-center gap-2 rounded-2xl px-5 py-3 font-black transition ${
            view === key
              ? "bg-emerald-400 text-slate-950"
              : "bg-slate-950 text-slate-400 hover:text-emerald-300"
          }`}
        >
          <Icon className="h-4 w-4" />
          {label}
        </button>
      ))}
    </div>
  );
}

function Dashboard({
  data,
  chartData,
  overallLevel,
  overallScore,
  likelihood,
  impact,
  loading,
}: {
  data: AnalyzeResponse | null;
  chartData: { name: string; score: number }[];
  overallLevel: string;
  overallScore: number;
  likelihood: number;
  impact: number;
  loading: boolean;
}) {
  if (!data && !loading) {
    return (
      <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-10 text-center">
        <ShieldCheck className="mx-auto h-12 w-12 text-emerald-300" />
        <h2 className="mt-4 text-2xl font-black">Ready for AI Risk Analysis</h2>
        <p className="mt-2 text-slate-400">
          Submit a scenario to activate the full multi-agent risk pipeline.
        </p>
      </section>
    );
  }

  if (loading) {
    return (
      <section className="mt-6 rounded-3xl border border-emerald-400/20 bg-slate-900/80 p-10 text-center">
        <Loader2 className="mx-auto h-12 w-12 animate-spin text-emerald-300" />
        <h2 className="mt-4 text-2xl font-black">Generating enterprise assessment...</h2>
        <p className="mt-2 text-slate-400">
          Retrieving NIST context, running agents, scoring risk, and preparing dashboard.
        </p>
      </section>
    );
  }

  return (
    <section className="mt-6 space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <Metric icon={<AlertTriangle />} label="Overall Risk" value={overallLevel} />
        <Metric icon={<Gauge />} label="Risk Score" value={`${overallScore}/100`} />
        <Metric icon={<Activity />} label="Likelihood" value={`${likelihood}/100`} />
        <Metric icon={<Zap />} label="Impact" value={`${impact}/100`} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Panel title="NIST Function Scores" icon={<Activity className="h-5 w-5" />}>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="score" fill="#34d399" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Risk Radar" icon={<RadarIcon className="h-5 w-5" />}>
          <ResponsiveContainer width="100%" height={320}>
            <RadarChart data={chartData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="name" stroke="#cbd5e1" />
              <PolarRadiusAxis domain={[0, 100]} stroke="#64748b" />
              <Radar dataKey="score" stroke="#34d399" fill="#34d399" fillOpacity={0.35} />
            </RadarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <Panel title="Risk Intelligence Summary" icon={<Brain className="h-5 w-5" />}>
          <p className="text-sm leading-7 text-slate-300">
            {data?.risk_score.scoring_rationale || "No scoring rationale returned."}
          </p>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-700 bg-slate-950 p-4">
              <h4 className="font-black text-emerald-300">Executive Decision</h4>
              <p className="mt-2 text-sm text-slate-300">
                {data?.risk_score.executive_decision || "Review required"}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-700 bg-slate-950 p-4">
              <h4 className="font-black text-emerald-300">Top Risk Categories</h4>
              <ul className="mt-2 space-y-1 text-sm text-slate-300">
                {(data?.risk_score.top_risk_categories || []).map((item) => (
                  <li key={item}>• {item}</li>
                ))}
              </ul>
            </div>
          </div>
        </Panel>

        <RiskMatrix likelihood={likelihood} impact={impact} />
      </div>
    </section>
  );
}

function Report({
  sections,
  raw,
}: {
  sections: { title: string; body: string }[];
  raw: string;
}) {
  if (!raw) {
    return (
      <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-10 text-center text-slate-400">
        No report generated yet.
      </section>
    );
  }

  return (
    <section className="mt-6 grid gap-6 lg:grid-cols-[280px_1fr]">
      <aside className="h-fit rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
        <h3 className="mb-4 font-black text-emerald-300">Sections</h3>
        <div className="space-y-2">
          {sections.map((section) => (
            <a
              key={section.title}
              href={`#${slug(section.title)}`}
              className="block rounded-xl bg-slate-950 px-4 py-3 text-sm font-bold text-slate-300 hover:text-emerald-300"
            >
              {section.title}
            </a>
          ))}
        </div>
      </aside>

      <div className="space-y-5">
        {sections.map((section) => (
          <article
            key={section.title}
            id={slug(section.title)}
            className="rounded-3xl border border-slate-200 bg-slate-50 p-7 text-slate-950"
          >
            <h2 className="mb-4 text-2xl font-black">{section.title}</h2>
            <div className="whitespace-pre-wrap text-sm leading-7 text-slate-800">
              {clean(section.body)}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function Architecture() {
  const items = [
    ["React Frontend", "Interactive dashboard and report workspace"],
    ["FastAPI Backend", "API layer for analysis and PDF export"],
    ["Agent Orchestrator", "Coordinates specialist AI risk agents"],
    ["Azure AI Search", "Retrieves NIST AI RMF context"],
    ["Azure OpenAI", "Generates analysis and risk scoring"],
    ["Azure Key Vault", "Protects service credentials"],
  ];

  return (
    <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
      <h2 className="text-2xl font-black">Full-Stack Architecture</h2>
      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map(([title, body], index) => (
          <div key={title} className="rounded-2xl border border-slate-700 bg-slate-950 p-5">
            <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-400 text-slate-950 font-black">
              {index + 1}
            </div>
            <h3 className="font-black text-white">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">{body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function Metric({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <div className="mb-3 text-emerald-300">{icon}</div>
      <p className="text-xs font-black uppercase tracking-[0.2em] text-slate-500">
        {label}
      </p>
      <p className="mt-2 text-2xl font-black text-white">{value}</p>
    </div>
  );
}

function Panel({
  title,
  icon,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-4 flex items-center gap-3">
        <div className="text-emerald-300">{icon}</div>
        <h3 className="text-xl font-black">{title}</h3>
      </div>
      {children}
    </div>
  );
}

function RiskMatrix({ likelihood, impact }: { likelihood: number; impact: number }) {
  const x = likelihood < 34 ? 0 : likelihood < 67 ? 1 : 2;
  const y = impact < 34 ? 0 : impact < 67 ? 1 : 2;

  return (
    <Panel title="Likelihood × Impact" icon={<AlertTriangle className="h-5 w-5" />}>
      <div className="grid grid-cols-4 gap-2 text-center text-xs font-black">
        <div />
        {["Low", "Medium", "High"].map((label) => (
          <div key={`likelihood-header-${label}`} className="text-slate-400">
            {label}
          </div>
        ))}

        {["High", "Medium", "Low"].map((impactLabel, row) => {
          const actualY = 2 - row;

          return (
            <div key={`risk-row-${impactLabel}`} className="contents">
              <div className="flex items-center justify-center text-slate-400">
                {impactLabel}
              </div>

              {[0, 1, 2].map((col) => {
                const active = x === col && y === actualY;
                const severity = actualY + col;

                return (
                  <div
                    key={`risk-cell-${impactLabel}-${col}`}
                    className={`flex h-20 items-center justify-center rounded-xl border ${
                      active
                        ? "border-emerald-300 bg-emerald-400 text-slate-950"
                        : severity >= 4
                        ? "border-red-400/20 bg-red-500/15 text-red-200"
                        : severity >= 3
                        ? "border-amber-400/20 bg-amber-500/15 text-amber-100"
                        : "border-emerald-400/10 bg-emerald-400/10 text-emerald-100"
                    }`}
                  >
                    {active ? "AI RISK" : severity + 1}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>

      <p className="mt-4 text-sm text-slate-400">
        Based on likelihood {likelihood}/100 and impact {impact}/100.
      </p>
    </Panel>
  );
}

function parseReport(markdown: string) {
  if (!markdown) return [];

  const sections: { title: string; body: string }[] = [];
  const lines = markdown.split("\n");

  let title = "Overview";
  let body: string[] = [];

  for (const line of lines) {
    if (line.startsWith("## ")) {
      if (body.length) sections.push({ title, body: body.join("\n").trim() });
      title = line.replace("## ", "").trim();
      body = [];
    } else if (!line.startsWith("# ")) {
      body.push(line);
    }
  }

  if (body.length) sections.push({ title, body: body.join("\n").trim() });

  return sections;
}

function clean(text: string) {
  return text.replace(/\*\*/g, "");
}

function slug(text: string) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-");
}