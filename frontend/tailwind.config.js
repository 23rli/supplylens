/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      colors: {
        brand: {
          50: "#eef2ff", 100: "#e0e7ff", 500: "#6366f1",
          600: "#4f46e5", 700: "#4338ca",
        },
        ink: { DEFAULT: "#1a2332", soft: "#5b6678", muted: "#8a94a6" },
        surface: { DEFAULT: "#ffffff", sunken: "#f6f8fb", border: "#e5e9f0" },
      },
      boxShadow: {
        card: "0 1px 2px 0 rgba(16,24,40,.04), 0 1px 3px 0 rgba(16,24,40,.06)",
        pop: "0 4px 12px -2px rgba(16,24,40,.10)",
      },
    },
  },
  plugins: [],
}
