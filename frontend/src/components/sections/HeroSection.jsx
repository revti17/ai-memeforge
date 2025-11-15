import { motion } from "framer-motion";

const highlightWords = ["teams", "creators", "brands"];

export function HeroSection({ onGenerate }) {
  return (
    <section className="relative overflow-hidden pt-20" id="product">
      <div className="mx-auto flex max-w-6xl flex-col items-center px-6 text-center">
        <motion.span
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/5 px-4 py-1 text-xs uppercase tracking-[0.3em] text-slate-300"
        >
          Premium AI Meme Studio
        </motion.span>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mt-6 text-balance text-4xl font-bold leading-tight text-white md:text-6xl"
        >
          Design viral memes your community will pay attention to.
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-6 max-w-2xl text-balance text-lg text-slate-300 md:text-xl"
        >
          MemeForge orchestrates top-tier visuals, captions, and trend intelligence so{" "}
          <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text font-semibold text-transparent">
            {highlightWords.join(", ")}
          </span>{" "}
          can publish culturally tuned content in seconds.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-10 flex flex-col items-center gap-4 md:flex-row"
        >
          <button
            onClick={onGenerate}
            className="rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 px-8 py-3 text-sm font-semibold uppercase tracking-wider text-white shadow-lg shadow-purple-500/40 transition hover:brightness-110"
          >
            Launch Studio
          </button>
          <div className="flex items-center gap-3 text-left">
            <div className="flex -space-x-2">
              {Array.from({ length: 4 }).map((_, idx) => (
                <span
                  key={idx}
                  className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-900 bg-slate-800 text-xs font-semibold text-white"
                >
                  {["JT", "AL", "MS", "+9"][idx]}
                </span>
              ))}
            </div>
            <p className="text-xs text-slate-400">
              Trusted by growth teams at Series A–C startups and global brands.
            </p>
          </div>
        </motion.div>
      </div>
      <div className="mx-auto mt-16 grid max-w-5xl gap-4 px-6 md:grid-cols-3">
        {[
          {
            metric: "3.1M+",
            label: "Monthly impressions driven by MemeForge campaigns",
          },
          {
            metric: "84%",
            label: "Faster go-to-market vs. traditional design workflows",
          },
          {
            metric: "22 countries",
            label: "Teams executing multi-lingual cultural drops",
          },
        ].map((item) => (
          <div
            key={item.metric}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-lg shadow-purple-500/10"
          >
            <p className="text-3xl font-semibold text-white">{item.metric}</p>
            <p className="mt-3 text-sm text-slate-300">{item.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}


