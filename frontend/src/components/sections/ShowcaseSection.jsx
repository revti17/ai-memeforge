import { motion } from "framer-motion";

export function ShowcaseSection({ generator }) {
  const {
    imageUrl,
    downloadUrl,
    filename,
    selectedCaption,
    palette,
    loading,
  } = generator.state;
  const { downloadMeme, resetOutput } = generator.actions;

  return (
    <section className="mt-24" id="showcase">
      <div className="mx-auto grid max-w-6xl gap-10 px-6 lg:grid-cols-[1.1fr_0.9fr]">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-3xl border border-white/10 bg-slate-900/70 shadow-2xl shadow-purple-500/10"
        >
          <div className="absolute right-6 top-6 rounded-full border border-white/20 bg-white/10 px-4 py-1 text-xs uppercase tracking-[0.3em] text-slate-300">
            Live Render
          </div>
          <div className="grid h-full place-items-center p-12">
            {imageUrl ? (
              <img
                src={imageUrl}
                alt="Generated meme preview"
                className="max-h-[500px] w-full rounded-2xl object-contain shadow-xl shadow-black/30"
              />
            ) : (
              <div className="flex flex-col items-center text-center text-slate-400">
                <span className="text-5xl">✨</span>
                <p className="mt-3 text-lg font-semibold text-white">
                  Your premium meme lands here
                </p>
                <p className="mt-2 max-w-sm text-sm text-slate-400">
                  Craft a prompt and we’ll generate a cinematic visual + optimized caption tuned for your audience.
                </p>
              </div>
            )}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          viewport={{ once: true }}
          className="flex flex-col justify-between gap-6 rounded-3xl border border-white/10 bg-slate-900/60 p-8 shadow-2xl shadow-purple-500/10"
        >
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">
              Delivery Package
            </p>
            <h3 className="mt-3 text-2xl font-semibold text-white">Export-ready asset suite</h3>
            <p className="mt-2 text-sm text-slate-300">
              Download high-res PNGs, social crops, and caption copy. Auto-sync with Buffer, Sprout, and Notion (coming soon).
            </p>
          </div>

          <div className="space-y-4 rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs font-medium uppercase tracking-widest text-slate-400">Headline</p>
            <p className="text-sm text-white">{selectedCaption || "Lock a caption to preview final copy."}</p>
          </div>

          <div className="space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3">
              <span>Export format</span>
              <span className="text-white">PNG • 2048px</span>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3">
              <span>File name</span>
              <span className="text-white">{filename || "—"}</span>
            </div>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              onClick={downloadMeme}
              disabled={!downloadUrl || loading}
              style={{ backgroundImage: palette.gradient }}
              className="flex-1 rounded-full px-6 py-3 text-sm font-semibold uppercase tracking-[0.3em] text-white shadow-lg shadow-purple-500/30 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Download Pro Assets
            </button>
            <button
              onClick={resetOutput}
              className="flex-1 rounded-full border border-white/10 px-6 py-3 text-sm font-semibold uppercase tracking-[0.3em] text-slate-200 transition hover:border-white/40 hover:text-white"
            >
              Generate Again
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}


