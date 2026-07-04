import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./web/index.html", "./web/src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#f4efe6",
        ink: "#1d2a36",
        accent: "#915c31",
        signal: "#c96e3d",
        mist: "#d8dfdf",
        pine: "#36534f",
      },
      fontFamily: {
        sans: ['"Avenir Next"', '"Segoe UI"', "sans-serif"],
        serif: ['"Iowan Old Style"', '"Palatino Linotype"', "Georgia", "serif"],
      },
      boxShadow: {
        panel: "0 20px 60px rgba(29, 42, 54, 0.12)",
      },
      backgroundImage: {
        paper:
          "radial-gradient(circle at top left, rgba(201,110,61,0.16), transparent 35%), linear-gradient(135deg, rgba(255,255,255,0.92), rgba(232,236,233,0.88))",
      },
    },
  },
  plugins: [],
};

export default config;
