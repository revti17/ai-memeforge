import { motion } from "framer-motion";

const testimonials = [
  {
    quote:
      "We replaced a four-agency roster with MemeForge. The turnarounds are instant and performance keeps climbing.",
    name: "Talia Cho",
    role: "VP Growth, Kinetic Labs",
  },
  {
    quote:
      "Every meme feels on-brand and culturally sharp. Our community actually asks how we’re shipping so fast.",
    name: "Marcus Reed",
    role: "Head of Social, Vault Finance",
  },
  {
    quote:
      "The analytics loop is a cheat code. MemeForge tells us what to ship next—our team just presses go.",
    name: "Priya Mehta",
    role: "Creative Director, Holo Snacks",
  },
];

export function TestimonialsSection() {
  return (
    <section className="mt-28" id="insights">
      <div className="mx-auto max-w-6xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mx-auto max-w-3xl text-center"
        >
          <span className="text-xs uppercase tracking-[0.4em] text-purple-300">Social proof</span>
          <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">Loved by category-defining teams</h2>
          <p className="mt-4 text-sm text-slate-300">
            MemeForge powers creative workflows at startups, consumer brands, and agencies leading the culture charge.
          </p>
        </motion.div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 shadow-2xl shadow-purple-500/10"
            >
              <p className="text-sm text-slate-200">“{testimonial.quote}”</p>
              <div className="mt-6 text-xs uppercase tracking-[0.3em] text-slate-400">
                {testimonial.name}
              </div>
              <div className="mt-1 text-xs text-slate-500">{testimonial.role}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}


