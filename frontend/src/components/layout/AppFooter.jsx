export function AppFooter() {
  const links = [
    { label: "Product", href: "#product" },
    { label: "Pricing", href: "#pricing" },
    { label: "Case Studies", href: "#insights" },
    { label: "Roadmap", href: "#" },
    { label: "Status", href: "#" },
  ];

  return (
    <footer className="mt-32 border-t border-white/10 bg-slate-950/80">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-12 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-blue-500 text-lg font-semibold text-white">
              AF
            </span>
            <div>
              <p className="text-sm uppercase tracking-widest text-slate-400">AI MemeForge</p>
              <p className="text-xs text-slate-500">Premium meme studio for cultural storytellers</p>
            </div>
          </div>
          <p className="mt-6 max-w-sm text-xs text-slate-500">
            Join the teams shaping tomorrow’s internet culture. Backed by world-class investors and trusted by global brands.
          </p>
        </div>
        <div className="flex flex-col items-start gap-4 text-sm text-slate-300 md:flex-row md:items-center">
          {links.map((item) => (
            <a key={item.label} href={item.href} className="transition hover:text-white">
              {item.label}
            </a>
          ))}
        </div>
      </div>
      <div className="border-t border-white/5 py-6 text-center text-xs text-slate-500">
        © {new Date().getFullYear()} MemeForge Labs. Crafted with wildly overcaffeinated AI.
      </div>
    </footer>
  );
}


