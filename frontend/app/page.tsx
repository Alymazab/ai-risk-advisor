"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  ShieldCheck,
  Brain,
  Activity,
  FileText,
  Loader2,
  AlertTriangle,
} from "lucide-react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
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

const API_URL = "http://127.0.0.1:8001/analyze";

export default function Home() {
  const [scenario, setScenario] = useState(
    "Assess the AI risks of deploying a customer-facing AI chatbot for a financial services company."
  );
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function runAnalysis() {
    setLoading(true);
    setData(null);

    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ scenario }),
    });

    const json = await res.json();
    setData(json);
    setLoading(false);
  }

  const chartData = data
    ? Object.entries(data.function_scores).map(([name, score]) => ({
        name,
        score,
      }))
    : [];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-3xl border border-emerald-400/30 bg-gradient-to-br from-slate-900 to-slate-800 p-8 shadow-2xl shadow-emerald-500/10"
        >
          <div className="mb-4 flex flex-wrap gap-2">
            {["Azure OpenAI", "Azure AI Search", "Key Vault", "NIST AI RMF", "FastAPI"].map(
              (item) => (
                <span
                  key={item}
                  className="rounded-full border border-emerald-400/40 bg-emerald-400/10 px-3 py-1 text-sm font-bold text-emerald-300"
                >
                  {item}
                </span>
              )
            )}
          </div>

          <h1 className="text-5xl font-black tracking-tight text-white md:text-6xl">
            AI Risk Advisor
          </h1>

          <p className="mt-4 max-w-3xl text-lg text-slate-300">
            Full-stack Azure AI governance platform for generating NIST AI RMF
            risk reports, scoring AI systems, and visualizing enterprise risk
            posture.
          </p>
        </motion.div>

        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
            <ShieldCheck className="mb-3 h-7 w-7 text-emerald-400" />
            <h3 className="text-lg font-bold">Governance-Aligned</h3>
            <p className="mt-2 text-sm text-slate-400">
              Uses GOVERN, MAP, MEASURE, and MANAGE agents aligned with NIST AI RMF.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
            <Brain className="mb-3 h-7 w-7 text-emerald-400" />
            <h3 className="text-lg font-bold">Multi-Agent Backend</h3>
            <p className="mt-2 text-sm text-slate-400">
              FastAPI connects the frontend to Azure OpenAI, AI Search, and Key Vault.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
            <Activity className="mb-3 h-7 w-7 text-emerald-400" />
            <h3 className="text-lg font-bold">Enterprise Dashboard</h3>
            <p className="mt-2 text-sm text-slate-400">
              Scores, radar charts, bar charts, executive decisions, and report output.
            </p>
          </div>
        </div>

        <section className="mt-8 rounded-3xl border border-slate-700 bg-slate-900 p-6">
          <h2 className="text-2xl font-black">Analyze an AI Scenario</h2>

          <textarea
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="mt-4 h-36 w-full rounded-2xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none focus:border-emerald-400"
          />

          <button
            onClick={runAnalysis}
            disabled={loading}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl bg-emerald-400 px-6 py-4 font-black text-slate-950 shadow-lg shadow-emerald-400/30 transition hover:bg-emerald-300 disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Running Multi-Agent Analysis...
              </>
            ) : (
              <>
                <ShieldCheck className="h-5 w-5" />
                Generate AI Risk Report
              </>
            )}
          </button>
        </section>

        {data && (
          <section className="mt-8 grid gap-6">
            <div className="grid gap-4 md:grid-cols-4">
              <Metric
                label="Overall Risk"
                value={data.risk_score.overall_risk_level || "Unknown"}
              />
              <Metric
                label="Risk Score"
                value={`${data.risk_score.overall_score || 0}/100`}
              />
              <Metric
                label="Likelihood"
                value={`${data.risk_score.likelihood_score || 0}/100`}
              />
              <Metric
                label="Impact"
                value={`${data.risk_score.impact_score || 0}/100`}
              />
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6">
                <h3 className="mb-4 text-xl font-black">NIST Function Scores</h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <XAxis dataKey="name" stroke="#94a3b8" />
                      <YAxis stroke="#94a3b8" domain={[0, 100]} />
                      <Tooltip />
                      <Bar dataKey="score" fill="#34d399" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6">
                <h3 className="mb-4 text-xl font-black">Risk Radar</h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={chartData}>
                      <PolarGrid stroke="#334155" />
                      <PolarAngleAxis dataKey="name" stroke="#cbd5e1" />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#64748b" />
                      <Radar
                        dataKey="score"
                        stroke="#34d399"
                        fill="#34d399"
                        fillOpacity={0.35}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              <div className="rounded-3xl border border-emerald-400/30 bg-slate-900 p-6 lg:col-span-1">
                <AlertTriangle className="mb-3 h-7 w-7 text-emerald-400" />
                <h3 className="text-xl font-black">Executive Decision</h3>
                <p className="mt-3 text-slate-300">
                  {data.risk_score.executive_decision || "Review required"}
                </p>

                <h4 className="mt-6 font-bold text-emerald-300">
                  Top Risk Categories
                </h4>
                <ul className="mt-2 list-disc pl-5 text-sm text-slate-300">
                  {(data.risk_score.top_risk_categories || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 lg:col-span-2">
                <FileText className="mb-3 h-7 w-7 text-emerald-400" />
                <h3 className="text-xl font-black">Scoring Rationale</h3>
                <p className="mt-3 text-slate-300">
                  {data.risk_score.scoring_rationale || "No rationale returned."}
                </p>
              </div>
            </div>

            <div className="rounded-3xl border border-slate-700 bg-slate-100 p-8 text-slate-950">
              <h2 className="mb-4 text-2xl font-black">Advisory Report</h2>
              <pre className="whitespace-pre-wrap text-sm leading-6">
                {data.report}
              </pre>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-emerald-400/20 bg-slate-900 p-5 shadow-lg shadow-emerald-400/5">
      <p className="text-sm font-bold text-slate-400">{label}</p>
      <p className="mt-2 text-2xl font-black text-white">{value}</p>
    </div>
  );
}