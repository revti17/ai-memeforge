import { motion } from "framer-motion";
import { SparklesIcon, ChartBarIcon, UsersIcon, ShieldCheckIcon } from "@heroicons/react/24/outline";

const features = [
  {
    title: "Adaptive Creative Engine",
    description:
      "OpenRouter + Flux stack fine-tunes visuals and tone to your brand system. No canned templates—every meme is orchestrated from scratch.",
    icon: SparklesIcon,
  },
  {
    title: "Audience Intelligence",
    description:
      "Live-trend ingestion from social and news signals informs prompts, hashtags, and timing recommendations suited to your niche.",
    icon: ChartBarIcon,
  },
  {
    title: "Team & Workflow Ready",
    description:
      "Invite collaborators, approve captions, leave notes, and sync final assets to Slack, Notion, or Miro boards instantly.",
    icon: UsersIcon,
  },
  {
    title: "Enterprise Guardrails",
    description:
      "Safety filters, brand compliance, and SOC2-ready audit logging keep legal teams comfortable while creative teams move fast.",
    icon: ShieldCheckIcon,
  },
];

export function FeatureSection() {
  return (
    <section className="mt-28" id="features">
      <div className="mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mx-auto max-w-3xl text-center"
        >
          <span className="text-xs uppercase tracking-[0.4em] text-purple-300">Capabilities</span>
          <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
            Built for modern growth teams that demand craft
          </h2>
          <p className="mt-4 text-sm text-slate-300">
            Studio-grade tooling, collaborative workflows, and actionable intelligence—all inside the fastest
            meme pipeline on the internet.
          </p>
        </motion.div>

        <div className="mt-10 grid gap-6 md:grid-cols-2">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              viewport={{ once: true }}
              className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 shadow-2xl shadow-purple-500/10"
            >
              <feature.icon className="h-9 w-9 text-purple-300" />
              <h3 className="mt-4 text-xl font-semibold text-white">{feature.title}</h3>
              <p className="mt-3 text-sm text-slate-300">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}


