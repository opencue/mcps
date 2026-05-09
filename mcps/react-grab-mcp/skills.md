# react-grab-mcp skills

Related skills from the `soul/skills` registry.

MCP source: [https://www.npmjs.com/package/@react-grab/mcp](https://www.npmjs.com/package/@react-grab/mcp)

Homepage: [https://www.npmjs.com/package/@react-grab/mcp](https://www.npmjs.com/package/@react-grab/mcp)

Package: `@react-grab/mcp`

Install: `npx -y @react-grab/mcp --stdio`

Expected type: `stdio`

Health command: `npx -y @react-grab/mcp --help`

Owners: `react-grab`

Agent surfaces: `codex`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `design-taste-frontend` | `design` | explicit | Use when building React/Next.js UI and the user asks for high-taste frontend, Tailwind components, motion-rich pages, or "design like a real engineer". Enforces dependency checks, RSC/client boundaries, Tailwind version rules, no-emoji policy, viewport-stable layouts, and tuned variance/motion/density baselines. |
| `image-to-code` | `design` | explicit | Use when user wants a website built from a design image, asks to "design then code", or wants section-by-section landing/marketing/portfolio pages. Generates per-section reference images first, analyzes them, then implements matching frontend. Forces large readable images per section, no card-in-card spam, and clean spacious hero composition. |
| `redesign-existing-projects` | `design` | explicit | Use when user says "redesign", "upgrade this site", "make this look better", "fix the design", or "audit my UI". Scans an existing project, diagnoses generic AI design patterns (default fonts, weak hierarchy, boring layouts), and applies targeted typography/spacing/color/motion fixes in place. Works with Tailwind, vanilla CSS, styled-components. |
| `visual-ralph` | `orchestration` | explicit | [OMX] Visual Ralph orchestration for frontend UI from generated references, static references, or live URL targets, using $ralph with $visual-verdict and pixel-diff evidence until the implementation matches and leaves a reproducible design system. |
| `visual-verdict` | `design` | explicit | Use when comparing a generated UI screenshot against one or more reference images and you need a deterministic pass/fail signal. Returns strict JSON `{score, verdict, category_match, differences, suggestions, reasoning}` with a 90+ pass threshold to drive the next edit iteration in visual-fidelity loops. |
