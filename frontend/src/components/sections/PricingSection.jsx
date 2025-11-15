import { motion } from "framer-motion";

const plans = [
  {
    name: "Creator",
    price: "$29",
    cadence: "per month",
    description: "Solo builders launching consistent cultural drops.",
    features: ["120 AI renders / month", "1 brand kit & logo memory", "Caption intelligence + auto hashtags", "Basic analytics"],
    highlighted: false,
  },
  {
    name: "Growth Team",
    price: "$89",
    cadence: "per month",
    description: "Marketing squads collaborating on multi-channel campaigns.",
    features: ["600 AI renders / month", "5 brand kits & style presets", "Team workspaces + approvals", "Advanced analytics & exports"],
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "Let's talk",
    cadence: "",
    description: "Global brands, agencies, and marketplaces.",
    features: ["Unlimited renders & variations", "SOC2 & compliance guardrails", "SSO / SCIM provisioning", "Dedicated success architect"],
    highlighted: false,
  },
];

export function PricingSection() {
  return (
    <section className="mt-28" id="pricing">
      <div className="mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mx-auto max-w-3xl text-center"
        >
          <span className="text-xs uppercase tracking-[0.4em] text-purple-300">Pricing</span>
          <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">Scale creativity without scaling cost</h2>
          <p className="mt-4 text-sm text-slate-300">
            Start free, upgrade when you're ready to bring the entire team onboard. Every plan includes enterprise grade
            safety and support.
          </p>
        </motion.div>

        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              viewport={{ once: true }}
              className={`flex h-full flex-col justify-between rounded-3xl border border-white/10 bg-slate-900/60 p-6 shadow-2xl shadow-purple-500/10 ${
                plan.highlighted ? "ring-2 ring-purple-500/50" : ""
              }`}
            >
              <div>
                <p className="text-xs uppercase tracking-[0.4em] text-purple-300">{plan.name}</p>
                <p className="mt-4 text-4xl font-semibold text-white">
                  {plan.price}
                  <span className="ml-2 text-base font-normal text-slate-400">{plan.cadence}</span>
                </p>
                <p className="mt-4 text-sm text-slate-300">{plan.description}</p>
                <ul className="mt-6 space-y-3 text-sm text-slate-200">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2">
                      <span className="mt-1 inline-flex h-5 w-5 items-center justify-center rounded-full bg-purple-500/20 text-xs text-purple-200">
                        ✓
                      </span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <button
                className={`mt-8 w-full rounded-full px-5 py-3 text-sm font-semibold uppercase tracking-[0.3em] transition ${
                  plan.highlighted
                    ? "bg-white text-slate-900 shadow-xl"
                    : "border border-white/10 text-white hover:border-white/40"
                }`}
              >
                {plan.highlighted ? "Start your 14-day trial" : "Talk to sales"}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}


