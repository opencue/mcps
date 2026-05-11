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
| `higgsfield-to-medusa-products` | `medusa` | prefix | Use when user says "Higgsfield to Medusa", "generate product photos", or "import AI product assets" and needs the Higgsfield-to-Medusa pipeline. Covers asset generation, product mapping, import, and validation.argument-hint: <shop> [<manifest.json>] |
| `imagegen-frontend-mobile` | `design` | explicit | Use when user says "mobile mockup", "generate mobile UI", or "imagegen mobile" and needs mobile frontend visual generation. Covers prompts, constraints, assets, and review. |
| `imagegen-frontend-web` | `design` | explicit | Use when user says "web mockup", "generate website UI", or "imagegen web" and needs web frontend visual generation. Covers prompts, layout, assets, and visual review. |
