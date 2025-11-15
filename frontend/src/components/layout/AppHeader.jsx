import { useAuth } from "../../context/AuthContext";

const navItems = [
  { label: "Product", href: "#product" },
  { label: "Showcase", href: "#showcase" },
  { label: "Plans", href: "#pricing" },
  { label: "Insights", href: "#insights" },
];

export function AppHeader({ onDashboardClick }) {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-blue-500 text-lg font-semibold">
            AF
          </span>
          <div>
            <p className="text-sm uppercase tracking-widest text-slate-300">AI MemeForge</p>
            <p className="text-xs text-slate-500">Craft culture-moving content in seconds</p>
          </div>
        </div>
        <nav className="hidden items-center gap-6 md:flex">
          {navItems.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="text-sm font-medium text-slate-300 transition hover:text-white"
            >
              {item.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              {user?.picture && (
                <img
                  src={user.picture}
                  alt={user.name}
                  className="h-8 w-8 rounded-full border-2 border-purple-500"
                />
              )}
              <button
                onClick={onDashboardClick}
                className="hidden rounded-full border border-white/20 px-4 py-2 text-sm font-medium text-white transition hover:border-white/40 md:block"
              >
                Dashboard
              </button>
              <button
                onClick={logout}
                className="rounded-full bg-gradient-to-r from-purple-500 to-fuchsia-500 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-purple-500/30 transition hover:from-purple-400 hover:to-fuchsia-400"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <button className="hidden rounded-full border border-white/20 px-4 py-2 text-sm font-medium text-white transition hover:border-white/40 md:block">
                Sign In
              </button>
              <button className="rounded-full bg-gradient-to-r from-purple-500 to-fuchsia-500 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-purple-500/30 transition hover:from-purple-400 hover:to-fuchsia-400">
                Start Free Trial
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}


