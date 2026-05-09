# MedusaDocs skills

Related skills from the `recodeee/skills` registry.

MCP source: [https://docs.medusajs.com/mcp](https://docs.medusajs.com/mcp)

| Skill | Reason | Description |
| --- | --- | --- |
| `building-admin-dashboard-customizations` | prefix | Load automatically when planning, researching, or implementing Medusa Admin dashboard UI (widgets, custom pages, forms, tables, data loading, navigation). REQUIRED for all admin UI work in ALL modes (planning, implementation, exploration). Contains design patterns, component usage, and data loading patterns that MCP servers don't provide. |
| `building-storefronts` | prefix | Load automatically when planning, researching, or implementing Medusa storefront features (calling custom API routes, SDK integration, React Query patterns, data fetching). REQUIRED for all storefront development in ALL modes (planning, implementation, exploration). Contains SDK usage patterns, frontend integration, and critical rules for calling Medusa APIs. |
| `building-with-medusa` | prefix | Load automatically when planning, researching, or implementing ANY Medusa backend features (custom modules, API routes, workflows, data models, module links, business logic). REQUIRED for all Medusa backend work in ALL modes (planning, implementation, exploration). Contains architectural patterns, best practices, and critical rules that MCP servers don't provide. |
| `creating-internal-agents` | explicit | Use when building an internal admin-facing AI agent in a Medusa project. These agents are operated by merchants and store operators — not customers. Covers data models, module service, agent runtime (tools, system prompt, streamText), streaming API routes (NDJSON), and admin UI chat extensions. Load for any internal agent type: store operations assistant, product audit, cohort analysis, customer service tooling for support staff, etc. Do NOT use for customer-facing agents (storefront chatbots, buyer-side assistants). |
| `db-generate` | prefix | Generate database migrations for a Medusa module |
| `db-migrate` | prefix | Run database migrations in Medusa |
| `medusa-reference` | explicit | Medusa implementation guidance for backend and storefront work. Use when building or modifying Medusa workflows, subscribers, API routes, auth, data models, query logic, jobs, or storefront integrations. |
| `new-user` | explicit | Create an admin user in Medusa |
| `storefront-best-practices` | explicit | ALWAYS use this skill when working on ecommerce storefronts, online stores, shopping sites. Use for ANY storefront component including checkout pages, cart, payment flows, product pages, product listings, navigation, homepage, or ANY page/component in a storefront. CRITICAL for adding checkout, implementing cart, integrating Medusa backend, or building any ecommerce functionality. Framework-agnostic (Next.js, SvelteKit, TanStack Start, React, Vue). Provides patterns, decision frameworks, backend integration guidance. |
| `woocommerce-to-medusa-import` | explicit | Build or run WooCommerce product importers into Medusa v2 backends. Use when importing WooCommerce products, variations, categories, images, prices, inventory, or metadata into Medusa, especially repos with apps/backend. Includes safe secret handling, dry-run/idempotent import rules, Medusa workflow usage, and verification steps. |
