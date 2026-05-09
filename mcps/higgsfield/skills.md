# Higgsfield skills

Related skills from the `soul/skills` registry.

MCP source: [https://mcp.higgsfield.ai/mcp](https://mcp.higgsfield.ai/mcp)

Homepage: [https://higgsfield.ai](https://higgsfield.ai)

Install: `hosted endpoint; no local install`

Expected type: `hosted`

Health command: `url:https://mcp.higgsfield.ai/mcp`

Owners: `recodeee`

Agent surfaces: `codex`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `brandkit` | `design` | explicit | Use when user says "brand kit", "brand guidelines", "logo system", "identity deck", "visual identity", "brand world", or "brand board". Generates brand-guidelines presentation boards as images — logo concepts, mockups, typography, color, and brand applications across minimalist, editorial, dark-tech, luxury, gaming, and consumer styles. |
| `higgsfield-generate` | `higgsfield` | prefix | Use when user says 'generate image/video', 'animate this photo', 'image-to-video', 'remix/stylize this', 'create an ad', or 'UGC video'. Runs Higgsfield models and Marketing Studio. Chain with higgsfield-soul-id for face consistency. NOT for product photoshoots or marketplace cards. |
| `higgsfield-marketplace-cards` | `higgsfield` | prefix | Use when user asks for 'marketplace listing images', 'product detail cards', 'A+ content', 'Amazon/Shopee/eBay images', or sales-ready listing sets. Generates compliant main image plus secondary and A+ modules. NOT for generic brand photography — use higgsfield-product-photoshoot. |
| `higgsfield-product-photoshoot` | `higgsfield` | prefix | Use when user says 'product photo', 'studio shot', 'lifestyle image', 'hero banner', 'ad creative', 'virtual try-on', or wants brand/paid-social product visuals. Backend-enhanced prompts on GPT Image 2. NOT for marketplace listing cards (use higgsfield-marketplace-cards) or generic image-gen. |
| `higgsfield-soul-id` | `higgsfield` | prefix | Use when user says 'train my face', 'create my Soul', 'make my digital twin', or 'build my avatar'. One-time training of a Soul Character face model; returns reference_id used by higgsfield-generate. NOT for one-shot face swaps or generating images — use higgsfield-generate. |
| `imagegen-frontend-mobile` | `design` | explicit | Use when user asks for mobile app screen mockups, iOS/Android UI concepts, onboarding/auth/dashboard/chat/fintech/health screens, or multi-screen app flows. Generates images only (no code) of app screens framed inside subtle phone mockups with consistent palettes and readable hierarchy. NOT for websites or landing pages — use imagegen-frontend-web. |
| `imagegen-frontend-web` | `design` | explicit | Use when user asks for landing page mockups, marketing site references, hero/section images, or website design comps. Generates one horizontal image per section (8 sections = 8 images, never combined), with varied hero composition, varied CTAs, and a single consistent palette across all images. NOT for mobile apps — use imagegen-frontend-mobile. |
