import { motion } from "framer-motion";
import { useAuth } from "../../context/AuthContext";

const defaultTrendPresets = [
  "Crypto market memes",
  "Monday standup chaos",
  "Holiday launch teaser",
  "SaaS onboarding woes",
];

const tones = [
  { label: "Humorous", value: "humorous" },
  { label: "Bold", value: "bold" },
  { label: "Playful", value: "playful" },
  { label: "Clever", value: "clever" },
];

const voices = [
  { label: "Casual", value: "casual" },
  { label: "Hype", value: "energetic" },
  { label: "Sarcastic", value: "sarcastic" },
  { label: "Professional", value: "professional" },
];

export function GeneratorSection({ generator, trends }) {
  const { requireAuth } = useAuth();
  const {
    prompt,
    setPrompt,
    uploadLogo,
    tone,
    setTone,
    voice,
    setVoice,
    useTrends,
    setUseTrends,
    brandColor,
    setBrandColor,
    loading,
    error,
    captionOptions,
    selectedCaption,
    setSelectedCaption,
    palette,
  } = generator.state;
  const { generateMeme } = generator.actions;

  const trendPresets = trends?.length ? trends.slice(0, 4) : defaultTrendPresets;

  const handleGenerate = () => {
    // Check if user is authenticated before generating
    if (requireAuth()) {
      generateMeme();
    }
  };

  return (
    <section className="relative mt-24" id="studio">
      <div className="absolute inset-x-0 -top-20 h-64 bg-gradient-to-b from-transparent via-purple-500/10 to-transparent blur-3xl" />
      <div className="mx-auto grid max-w-6xl gap-10 px-6 lg:grid-cols-[1.25fr_1fr]">
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="rounded-3xl border border-white/10 bg-slate-900/60 p-8 shadow-2xl shadow-purple-500/10"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Creative Brief</h2>
            <label className="flex items-center gap-2 text-xs text-slate-300">
              <input
                type="checkbox"
                checked={useTrends}
                onChange={(e) => setUseTrends(e.target.checked)}
                className="h-4 w-4 rounded border-white/40 bg-transparent accent-purple-500"
              />
              Auto-inject trending keywords
            </label>
          </div>

          <div className="mt-6 space-y-5">
            <div>
                <div className="mb-2 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <label className="text-xs font-medium uppercase tracking-widest text-slate-400">
                  Narrative Prompt
                </label>
                <div className="flex flex-wrap gap-2">
                  {trendPresets.map((preset) => (
                    <button
                      key={preset}
                      onClick={() => setPrompt(preset)}
                      className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300 transition hover:border-white/40 hover:text-white"
                    >
                      {preset}
                    </button>
                  ))}
                </div>
              </div>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the vibe, characters, conflict, or punchline you want to deliver..."
                rows={4}
                className="w-full rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-sm text-white placeholder:text-slate-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
              />
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="md:col-span-2">
                <label className="text-xs font-medium uppercase tracking-widest text-slate-400">
                  Brand Personality
                </label>
                <div className="mt-3 flex flex-wrap gap-2">
                  {tones.map((option) => (
                    <button
                      key={option.value}
                      onClick={() => setTone(option.value)}
                      className={`rounded-full px-4 py-2 text-xs font-medium uppercase tracking-wide transition ${
                        tone === option.value
                          ? "bg-white text-slate-900"
                          : "border border-white/10 text-slate-300 hover:border-white/40 hover:text-white"
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs font-medium uppercase tracking-widest text-slate-400">
                  Voice Mood
                </label>
                <select
                  value={voice}
                  onChange={(e) => setVoice(e.target.value)}
                  className="mt-3 w-full rounded-xl border border-white/10 bg-slate-900/60 px-3 py-3 text-sm text-white focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/40"
                >
                  {voices.map((option) => (
                    <option key={option.value} value={option.value} className="bg-slate-900 text-white">
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-xs font-medium uppercase tracking-widest text-slate-400">
                  Brand Accent Color
                </label>
                <div className="mt-3 flex items-center gap-3">
                  <input
                    type="color"
                    value={brandColor}
                    onChange={(e) => setBrandColor(e.target.value)}
                    className="h-11 w-11 cursor-pointer appearance-none rounded-xl border border-white/10 bg-transparent p-1"
                  />
                  <div>
                    <p className="text-sm font-medium text-white">{brandColor}</p>
                    <p className="text-xs text-slate-400">Used for overlays & CTA treatments</p>
                  </div>
                </div>
              </div>
              <div>
                <label className="text-xs font-medium uppercase tracking-widest text-slate-400">
                  Upload Brand Logo
                </label>
                <div className="mt-3 rounded-xl border border-dashed border-white/20 p-4 text-center text-xs text-slate-400">
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    id="logo-upload"
                    onChange={(event) => uploadLogo(event.target.files?.[0] || null)}
                  />
                  <label htmlFor="logo-upload" className="cursor-pointer font-medium text-purple-300 hover:text-purple-200">
                    Drop logo or browse
                  </label>
                  <p className="mt-1 text-[10px] text-slate-500">PNG, SVG, JPG — max 5MB</p>
                </div>
              </div>
            </div>

            {error && (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                {error}
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={loading}
              style={{ backgroundImage: palette.gradient }}
              className="mt-2 flex w-full items-center justify-center gap-3 rounded-full px-6 py-3 text-sm font-semibold uppercase tracking-[0.3em] text-white shadow-xl shadow-purple-500/30 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Synthesizing your meme..." : "Generate Signature Meme"}
            </button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="flex h-full flex-col justify-between gap-6"
        >
          <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-purple-500/10">
            <p className="text-sm font-semibold uppercase tracking-[0.4em] text-slate-500">
              Caption Explorer
            </p>
            <p className="mt-2 text-sm text-slate-300">
              Swipe through AI recommendations and lock the headline before exporting.
            </p>
            <div className="mt-4 space-y-3">
              {captionOptions.length ? (
                captionOptions.map((caption) => (
                  <button
                    key={caption}
                    onClick={() => setSelectedCaption(caption)}
                    className={`w-full rounded-2xl border px-4 py-3 text-left text-sm transition ${
                      selectedCaption === caption
                        ? "border-transparent bg-white text-slate-900 shadow-lg"
                        : "border-white/10 bg-white/5 text-slate-300 hover:border-white/40 hover:text-white"
                    }`}
                  >
                    {caption}
                  </button>
                ))
              ) : (
                <div className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">
                  Generate a meme to see tailored captions and insights here.
                </div>
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 via-white/10 to-white/5 p-6 shadow-2xl shadow-purple-500/10">
            <p className="text-sm font-semibold uppercase tracking-[0.4em] text-slate-500">
              Delivery Insights
            </p>
            <ul className="mt-4 space-y-4 text-sm text-slate-300">
              <li className="flex items-start gap-3">
                <span className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-purple-500/20 text-purple-200">
                  1
                </span>
                <p>
                  AI-enhanced prompt engineering aligns visual storytelling with your brand tone automatically.
                </p>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-purple-500/20 text-purple-200">
                  2
                </span>
                <p>
                  Guardrails keep content on-brand and safe—each export is screened for tone, claims, and compliance.
                </p>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-purple-500/20 text-purple-200">
                  3
                </span>
                <p>
                  Engagement analytics benchmark performance vs. best-in-class memes across our network.
                </p>
              </li>
            </ul>
          </div>
        </motion.div>
      </div>
    </section>
  );
}


