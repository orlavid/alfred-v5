import { resolve } from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: "web",
  publicDir: "public",
  build: {
    outDir: "../dist",
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "web/src"),
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./web/src/test/setup.ts",
    css: true,
    globals: true,
  },
});
