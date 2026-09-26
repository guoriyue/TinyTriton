import { defineConfig } from "vitepress";

export default defineConfig({
  title: "TinyTriton",
  description: "Build a compiler in Python: Step 1, source code to instructions",
  base: "/TinyTriton/",
  rewrites: { "README.md": "index.md" },
  srcExclude: ["**/node_modules/**", "**/.venv/**"],
  cleanUrls: true,
  ignoreDeadLinks: [/\.py$/, /LICENSE$/],
  themeConfig: {
    nav: [
      { text: "Step 1", link: "/steps/step01-triton-ir" },
      { text: "Blog series", link: "https://guoriyue.github.io/blog/tinytriton-series/" },
      { text: "GitHub", link: "https://github.com/guoriyue/TinyTriton" },
    ],
    sidebar: [
      { text: "Start", link: "/" },
      { text: "1. Source to instructions", link: "/steps/step01-triton-ir" },
    ],
    outline: [2, 3],
    search: { provider: "local" },
  },
});
