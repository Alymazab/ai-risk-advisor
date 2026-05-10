"use client";

import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  Cpu,
  FileText,
  Gauge,
  Layers,
  Loader2,
  Lock,
  Network,
  Radar as RadarIcon,
  ShieldCheck,
  Sparkles,
  Terminal,
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

const API_URL = `${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"}/analyze`;

const exampleScenarios = [
  {
    title: "Financial AI Chatbot",
    scenario:
      "Assess the AI risks of deploying a customer-facing AI chatbot for a global financial services company that provides investment guidance, processes transactions, integrates with internal banking APIs, and handles sensitive customer data.",
  },
  {
    title: "Healthcare Copilot",
    scenario:
      "Assess the AI risks of deploying a generative AI copilot for a multinational healthcare organization that assists doctors with diagnosis recommendations, patient summarization, and treatment planning across multiple hospitals while integrating with electronic health record systems and third-party APIs.",
  },
  {
    title: "AI Hiring Assistant",
    scenario:
      "Assess the AI risks of deploying an AI hiring assistant that screens resumes, ranks candidates, and recommends hiring decisions for a large enterprise operating across multiple regions.",
  },
];

const agentSteps = [
  { name: "GOVERN", detail: "Governance, accountability, oversight", icon: ShieldCheck },
  { name: "MAP", detail: "Context, stakeholders, impacts", icon: Network },
  { name: "MEASURE", detail: "Testing, validation, monitoring", icon: Gauge },
  { name: "MANAGE", detail: "Mitigation, response, residual risk", icon: Activity },
  { name: "PLAYBOOK", detail: "NIST implementation guidance", icon: Layers },
  { name: "SCORE", detail: "LLM-based risk scoring", icon: Brain },
];

export default function Home() {
  const [scenario, setScenario] = useState(exampleScenarios[0].scenario);
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeView, setActiveView] = useState<"dashboard" | "report" | "architecture">(
    "dashboard"
  );
  const [error, setError] = useState<string | null>(null);

  async function runAnalysis() {
    setLoading(true);
    setData(null);
    setError(null);
    setActiveView("dashboard");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ scenario }),
      });

      if (!res.ok) {
        throw new Error(`API error ${res.status}`);
      }

      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred.");
    } finally {
      setLoading(false);
    }
  }

  const chartData = useMemo(() => {
    if (!data) return [];
    return Object.entries(data.function_scores || {}).map(([name, score]) => ({
      name,
      score,
    }));
  }, [data]);

  const reportSections = useMemo(() => parseMarkdownSections(data?.report || ""), [data]);

  const riskLevel = data?.risk_score.overall_risk_level || "Awaiting Analysis";
  const riskScore = data?.risk_score.overall_score ?? 0;
  const likelihood = data?.risk_score.likelihood_score ?? 0;
  const impact = data?.risk_score.impact_score ?? 0;

  return (
    <main className="min-h-screen overflow-hidden bg-[#020617] text-slate-100">
      <div className="pointer-events-none fixed inset-0 opacity-70">
        <div className="absolute left-[-10%] top-[-10%] h-[420px] w-[420px] rounded-full bg-emerald-500/20 blur-[120px]" />
        <div className="absolute right-[-10%] top-[20%] h-[500px] w-[500px] rounded-full bg-cyan-500/10 blur-[140px]" />
        <div className="absolute bottom-[-20%] left-[30%] h-[500px] w-[500px] rounded-full bg-lime-400/10 blur-[140px]" />
      </div>

      <div className="relative grid min-h-screen grid-cols-1 lg:grid-cols-[280px_1fr]">
        <aside className="hidden border-r border-emerald-400/10 bg-slate-950/80 p-6 backdrop-blur-xl lg:block">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl border border-emerald-400/40 bg-emerald-400/10 p-3 shadow-lg shadow-emerald-400/20">
              <ShieldCheck className="h-7 w-7 text-emerald-300" />
            </div>
            <div>
              <p className="text-lg font-black tracking-tight">AI Risk Advisor</p>
              <p className="text-xs font-bold uppercase tracking-[0.25em] text-emerald-300">
                Command Center
              </p>
            </div>
          </div>

          <div className="mt-8 rounded-3xl border border-emerald-400/10 bg-slate-900/70 p-4">
            <div className="flex items-center gap-2 text-sm font-bold text-emerald-300">
              <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_15px_#34d399]" />
              SYSTEM ONLINE
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-400">
              Multi-agent Azure AI governance platform aligned to NIST AI RMF.
            </p>
          </div>

          <nav className="mt-8 space-y-2">
            <NavButton
              active={activeView === "dashboard"}
              onClick={() => setActiveView("dashboard")}
              icon={<Activity className="h-4 w-4" />}
              label="Risk Dashboard"
            />
            <NavButton
              active={activeView === "report"}
              onClick={() => setActiveView("report")}
              icon={<FileText className="h-4 w-4" />}
              label="Advisory Report"
            />
            <NavButton
              active={activeView === "architecture"}
              onClick={() => setActiveView("architecture")}
              icon={<Cpu className="h-4 w-4" />}
              label="Architecture"
            />
          </nav>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/70 p-4">
            <p className="mb-3 text-xs font-black uppercase tracking-[0.2em] text-slate-500">
              Azure Stack
            </p>
            {["Azure OpenAI", "Azure AI Search", "Key Vault", "FastAPI", "Next.js"].map(
              (item) => (
                <div key={item} className="mb-2 flex items-center gap-2 text-sm text-slate-300">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  {item}
                </div>
              )
            )}
          </div>
        </aside>

        <section className="p-4 md:p-8">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-[2rem] border border-emerald-400/20 bg-slate-950/70 p-6 shadow-2xl shadow-emerald-500/10 backdrop-blur-xl md:p-8"
          >
            <div className="flex flex-col justify-between gap-6 xl:flex-row xl:items-center">
              <div>
                <div className="mb-4 flex flex-wrap gap-2">
                  {["NIST AI RMF", "Multi-Agent RAG", "Secure Azure AI", "Live API"].map(
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
                  Enterprise AI Risk Intelligence Platform
                </h1>

                <p className="mt-4 max-w-3xl text-base leading-7 text-slate-300 md:text-lg">
                  Analyze high-risk AI deployments with Azure-powered agents, NIST AI RMF
                  grounding, Playbook implementation guidance, executive scoring, and risk
                  visualizations.
                </p>
              </div>

              <div className="rounded-3xl border border-emerald-400/20 bg-slate-900 p-5 shadow-xl shadow-emerald-400/10">
                <p className="text-xs font-black uppercase tracking-[0.2em] text-slate-500">
                  Current Risk Posture
                </p>
                <div className="mt-3 flex items-end gap-3">
                  <p className="text-5xl font-black text-emerald-300">{riskScore}</p>
                  <p className="pb-2 text-slate-400">/100</p>
                </div>
                <RiskBadge level={riskLevel} />
              </div>
            </div>
          </motion.div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_420px]">
            <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6 backdrop-blur-xl">
              <div className="mb-5 flex items-center gap-3">
                <Sparkles className="h-6 w-6 text-emerald-300" />
                <h2 className="text-2xl font-black">Scenario Console</h2>
              </div>

              <div className="mb-4 grid gap-3 md:grid-cols-3">
                {exampleScenarios.map((item) => (
                  <button
                    key={item.title}
                    onClick={() => setScenario(item.scenario)}
                    className="rounded-2xl border border-emerald-400/10 bg-slate-900 p-4 text-left transition hover:border-emerald-400/40 hover:bg-emerald-400/10"
                  >
                    <p className="font-black text-white">{item.title}</p>
                    <p className="mt-2 line-clamp-3 text-xs leading-5 text-slate-400">
                      {item.scenario}
                    </p>
                  </button>
                ))}
              </div>

              <textarea
                value={scenario}
                onChange={(e) => setScenario(e.target.value)}
                className="h-44 w-full resize-none rounded-3xl border border-slate-800 bg-slate-900/80 p-5 text-sm leading-6 text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-emerald-400/60 focus:ring-4 focus:ring-emerald-400/10"
              />

              <button
                onClick={runAnalysis}
                disabled={loading}
                className="mt-4 flex w-full items-center justify-center gap-3 rounded-3xl bg-gradient-to-r from-emerald-400 to-lime-300 px-6 py-4 font-black text-slate-950 shadow-xl shadow-emerald-400/20 transition hover:scale-[1.01] hover:shadow-emerald-400/40 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Running AI Governance Pipeline...
                  </>
                ) : (
                  <>
                    <Zap className="h-5 w-5" />
                    Generate Enterprise Risk Assessment
                  </>
                )}
              </button>

              {error && (
                <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}
            </div>

            <AgentPipeline loading={loading} completed={!!data} />
          </div>

          {data ? (
            <div className="mt-6">
              {activeView === "dashboard" && (
                <DashboardView
                  data={data}
                  chartData={chartData}
                  likelihood={likelihood}
                  impact={impact}
                />
              )}

              {activeView === "report" && <ReportView sections={reportSections} raw={data.report} />}

              {activeView === "architecture" && <ArchitectureView />}
            </div>
          ) : (
            <EmptyState loading={loading} />
          )}
        </section>
      </div>
    </main>
  );
}

function DashboardView({
  data,
  chartData,
  likelihood,
  impact,
}: {
  data: AnalyzeResponse;
  chartData: { name: string; score: number }[];
  likelihood: number;
  impact: number;
}) {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard
          icon={<AlertTriangle className="h-5 w-5" />}
          label="Overall Risk"
          value={data.risk_score.overall_risk_level || "Unknown"}
        />
        <MetricCard
          icon={<Gauge className="h-5 w-5" />}
          label="Risk Score"
          value={`${data.risk_score.overall_score || 0}/100`}
        />
        <MetricCard
          icon={<Activity className="h-5 w-5" />}
          label="Likelihood"
          value={`${likelihood}/100`}
        />
        <MetricCard
          icon={<Zap className="h-5 w-5" />}
          label="Impact"
          value={`${impact}/100`}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <ChartCard title="NIST Function Risk Scores" icon={<Activity className="h-5 w-5" />}>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  background: "#020617",
                  border: "1px solid rgba(52,211,153,.25)",
                  borderRadius: "12px",
                  color: "#fff",
                }}
              />
              <Bar dataKey="score" fill="#34d399" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Risk Posture Radar" icon={<RadarIcon className="h-5 w-5" />}>
          <ResponsiveContainer width="100%" height={320}>
            <RadarChart data={chartData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="name" stroke="#cbd5e1" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#64748b" />
              <Radar dataKey="score" stroke="#34d399" fill="#34d399" fillOpacity={0.35} />
            </RadarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
          <div className="mb-5 flex items-center gap-3">
            <Terminal className="h-5 w-5 text-emerald-300" />
            <h3 className="text-xl font-black">Risk Intelligence Summary</h3>
          </div>

          <p className="text-sm leading-7 text-slate-300">
            {data.risk_score.scoring_rationale || "No scoring rationale returned."}
          </p>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-3xl border border-emerald-400/10 bg-slate-900 p-5">
              <h4 className="font-black text-emerald-300">Executive Decision</h4>
              <p className="mt-3 text-sm leading-6 text-slate-300">
                {data.risk_score.executive_decision || "Review required"}
              </p>
            </div>

            <div className="rounded-3xl border border-emerald-400/10 bg-slate-900 p-5">
              <h4 className="font-black text-emerald-300">Top Risk Categories</h4>
              <ul className="mt-3 space-y-2 text-sm text-slate-300">
                {(data.risk_score.top_risk_categories || []).map((item) => (
                  <li key={item} className="flex gap-2">
                    <span className="mt-2 h-1.5 w-1.5 rounded-full bg-emerald-400" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <RiskMatrix likelihood={likelihood} impact={impact} />
      </div>
    </div>
  );
}

function ReportView({ sections, raw }: { sections: { title: string; body: string }[]; raw: string }) {
  return (
    <div className="grid gap-6 xl:grid-cols-[320px_1fr]">
      <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-5">
        <h3 className="mb-4 font-black text-emerald-300">Report Sections</h3>
        <div className="space-y-2">
          {sections.map((section) => (
            <a
              key={section.title}
              href={`#${slug(section.title)}`}
              className="block rounded-2xl border border-slate-800 bg-slate-900 p-3 text-sm font-bold text-slate-300 transition hover:border-emerald-400/30 hover:text-emerald-300"
            >
              {section.title}
            </a>
          ))}
        </div>
      </div>

      <div className="space-y-5">
        {sections.length > 0 ? (
          sections.map((section) => (
            <section
              id={slug(section.title)}
              key={section.title}
              className="rounded-[2rem] border border-slate-800 bg-slate-100 p-7 text-slate-950 shadow-xl"
            >
              <h2 className="mb-4 text-2xl font-black">{section.title}</h2>
              <div className="whitespace-pre-wrap text-sm leading-7 text-slate-800">
                {cleanMarkdown(section.body)}
              </div>
            </section>
          ))
        ) : (
          <pre className="whitespace-pre-wrap rounded-[2rem] bg-slate-100 p-8 text-sm text-slate-950">
            {raw}
          </pre>
        )}
      </div>
    </div>
  );
}

function ArchitectureView() {
  const nodes = [
    ["React Dashboard", "Next.js frontend with charts and interactive UX"],
    ["FastAPI Backend", "API layer exposing /analyze for AI risk assessment"],
    ["Agent Orchestrator", "Runs GOVERN, MAP, MEASURE, MANAGE, Playbook, scoring"],
    ["Azure AI Search", "Retrieves NIST AI RMF framework context"],
    ["Azure OpenAI", "Generates agent outputs and executive synthesis"],
    ["Azure Key Vault", "Protects Azure OpenAI and Search credentials"],
  ];

  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
      <h2 className="mb-6 text-2xl font-black">Full-Stack Azure AI Architecture</h2>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {nodes.map(([title, desc], index) => (
          <motion.div
            key={title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06 }}
            className="rounded-3xl border border-emerald-400/10 bg-slate-900 p-5"
          >
            <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-400/10 text-emerald-300">
              {index + 1}
            </div>
            <h3 className="font-black text-white">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">{desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function AgentPipeline({ loading, completed }: { loading: boolean; completed: boolean }) {
  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6 backdrop-blur-xl">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black">Agent Pipeline</h2>
          <p className="mt-1 text-sm text-slate-400">Live orchestration view</p>
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
        {agentSteps.map((step, index) => {
          const Icon = step.icon;
          const active = loading;
          const done = completed;

          return (
            <motion.div
              key={step.name}
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={`rounded-2xl border p-4 transition ${
                done
                  ? "border-emerald-400/30 bg-emerald-400/10"
                  : active
                  ? "border-emerald-400/20 bg-slate-900"
                  : "border-slate-800 bg-slate-900/70"
              }`}
            >
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-slate-950 p-2 text-emerald-300">
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-black">{step.name}</p>
                  <p className="text-xs text-slate-400">{step.detail}</p>
                </div>
                <div className="ml-auto">
                  {done ? (
                    <CheckCircle2 className="h-5 w-5 text-emerald-300" />
                  ) : active ? (
                    <span className="block h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_14px_#34d399]" />
                  ) : (
                    <span className="block h-2.5 w-2.5 rounded-full bg-slate-700" />
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

function MetricCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-[1.6rem] border border-emerald-400/10 bg-slate-950/80 p-5 shadow-xl shadow-emerald-500/5">
      <div className="mb-3 flex items-center justify-between">
        <div className="rounded-2xl bg-emerald-400/10 p-2 text-emerald-300">{icon}</div>
      </div>
      <p className="text-xs font-black uppercase tracking-[0.2em] text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-black text-white">{value}</p>
    </div>
  );
}

function ChartCard({
  title,
  icon,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
      <div className="mb-4 flex items-center gap-3">
        <div className="rounded-2xl bg-emerald-400/10 p-2 text-emerald-300">{icon}</div>
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
    <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
      <h3 className="mb-4 text-xl font-black">Likelihood × Impact Matrix</h3>

      <div className="grid grid-cols-4 gap-2 text-center text-xs font-black">
        <div />
        {["Low", "Medium", "High"].map((label) => (
          <div key={label} className="text-slate-400">
            {label}
          </div>
        ))}

        {["High", "Medium", "Low"].map((impactLabel, rowIndex) => {
          const actualY = 2 - rowIndex;

          return (
            <>
              <div key={`${impactLabel}-label`} className="flex items-center justify-center text-slate-400">
                {impactLabel}
              </div>
              {[0, 1, 2].map((colIndex) => {
                const active = x === colIndex && y === actualY;
                const intensity = actualY + colIndex;

                return (
                  <div
                    key={`${impactLabel}-${colIndex}`}
                    className={`relative flex h-20 items-center justify-center rounded-2xl border ${
                      active
                        ? "border-emerald-300 bg-emerald-400 text-slate-950 shadow-lg shadow-emerald-400/30"
                        : intensity >= 4
                        ? "border-red-400/20 bg-red-500/20 text-red-200"
                        : intensity >= 3
                        ? "border-amber-400/20 bg-amber-500/20 text-amber-100"
                        : "border-emerald-400/10 bg-emerald-400/10 text-emerald-100"
                    }`}
                  >
                    {active ? "AI RISK" : intensity + 1}
                  </div>
                );
              })}
            </>
          );
        })}
      </div>

      <p className="mt-4 text-sm leading-6 text-slate-400">
        Current placement uses likelihood {likelihood}/100 and impact {impact}/100.
      </p>
    </div>
  );
}

function NavButton({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-bold transition ${
        active
          ? "bg-emerald-400 text-slate-950 shadow-lg shadow-emerald-400/20"
          : "text-slate-400 hover:bg-slate-900 hover:text-emerald-300"
      }`}
    >
      {icon}
      {label}
    </button>
  );
}

function RiskBadge({ level }: { level: string }) {
  const normalized = level.toLowerCase();
  const color =
    normalized.includes("critical") || normalized.includes("high")
      ? "border-red-400/30 bg-red-500/10 text-red-200"
      : normalized.includes("medium")
      ? "border-amber-400/30 bg-amber-500/10 text-amber-100"
      : normalized.includes("low")
      ? "border-emerald-400/30 bg-emerald-500/10 text-emerald-200"
      : "border-slate-700 bg-slate-800 text-slate-300";

  return (
    <div className={`mt-4 inline-flex rounded-full border px-3 py-1 text-xs font-black uppercase ${color}`}>
      {level}
    </div>
  );
}

function EmptyState({ loading }: { loading: boolean }) {
  if (loading) {
    return (
      <div className="mt-6 rounded-[2rem] border border-emerald-400/10 bg-slate-950/70 p-8 text-center">
        <Loader2 className="mx-auto h-10 w-10 animate-spin text-emerald-300" />
        <h3 className="mt-4 text-2xl font-black">Agents are analyzing the scenario...</h3>
        <p className="mt-2 text-slate-400">
          Retrieving NIST context, running specialist agents, scoring risk, and synthesizing the report.
        </p>
      </div>
    );
  }

  return (
    <div className="mt-6 rounded-[2rem] border border-slate-800 bg-slate-950/70 p-8 text-center">
      <Lock className="mx-auto h-10 w-10 text-emerald-300" />
      <h3 className="mt-4 text-2xl font-black">Awaiting AI risk scenario</h3>
      <p className="mt-2 text-slate-400">
        Submit a scenario to activate the multi-agent risk intelligence pipeline.
      </p>
    </div>
  );
}

function parseMarkdownSections(markdown: string) {
  if (!markdown) return [];

  const lines = markdown.split("\n");
  const sections: { title: string; body: string }[] = [];

  let currentTitle = "Overview";
  let currentBody: string[] = [];

  for (const line of lines) {
    if (line.startsWith("## ")) {
      if (currentBody.length > 0) {
        sections.push({ title: currentTitle, body: currentBody.join("\n").trim() });
      }
      currentTitle = line.replace("## ", "").trim();
      currentBody = [];
    } else if (!line.startsWith("# ")) {
      currentBody.push(line);
    }
  }

  if (currentBody.length > 0) {
    sections.push({ title: currentTitle, body: currentBody.join("\n").trim() });
  }

  return sections;
}

function cleanMarkdown(text: string) {
  return text.replace(/\*\*/g, "");
}

function slug(text: string) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-");
}