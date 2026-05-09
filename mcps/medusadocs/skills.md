# MedusaDocs skills

Related skills from the `soul/skills` registry.

MCP source: [https://docs.medusajs.com/mcp](https://docs.medusajs.com/mcp)

Homepage: [https://docs.medusajs.com](https://docs.medusajs.com)

Install: `hosted endpoint; no local install`

Expected type: `hosted`

Health command: `url:https://docs.medusajs.com/mcp`

Owners: `Medusa`

Agent surfaces: `codex`

| Skill | Category | Reason | Description |
| --- | --- | --- | --- |
| `building-admin-dashboard-customizations` | `medusa` | prefix | Load automatically when planning, researching, or implementing Medusa Admin dashboard UI (widgets, custom pages, forms, tables, data loading, navigation). REQUIRED for all admin UI work in ALL modes (planning, implementation, exploration). Contains design patterns, component usage, and data loading patterns that MCP servers don't provide. |
| `building-storefronts` | `medusa` | prefix | Load automatically when planning, researching, or implementing Medusa storefront features (calling custom API routes, SDK integration, React Query patterns, data fetching). REQUIRED for all storefront development in ALL modes (planning, implementation, exploration). Contains SDK usage patterns, frontend integration, and critical rules for calling Medusa APIs. |
| `building-with-medusa` | `medusa` | prefix | Load automatically when planning, researching, or implementing ANY Medusa backend features (custom modules, API routes, workflows, data models, module links, business logic). REQUIRED for all Medusa backend work in ALL modes (planning, implementation, exploration). Contains architectural patterns, best practices, and critical rules that MCP servers don't provide. |
| `creating-internal-agents` | `medusa` | explicit | Use when building an internal admin-facing AI agent in a Medusa project — operated by merchants/operators, NOT customers. Covers data models, module service, agent runtime (tools, system prompt, streamText), streaming NDJSON API routes, and admin UI chat extensions. NOT for storefront / buyer-side chatbots. |
| `db-generate` | `medusa` | prefix | Generate database migrations for a Medusa module via `npx medusa db:generate <module-name>`. Use when user says /medusa-dev:db-generate, generate migrations for module X, or modifies a Medusa module data model and needs migration files. Pair with /db-migrate to apply. |
| `db-migrate` | `medusa` | prefix | Apply pending Medusa database migrations via `npx medusa db:migrate`. Use when user says /medusa-dev:db-migrate, run migrations, apply pending migrations, or after running /db-generate to bring the database up to date. Reports applied count plus any errors. |
| `gh-submodule-publish` | `medusa` | category | Create missing GitHub repos and push a parent repo that tracks app repos as Git submodules. Use when user asks to publish locally-initialized repos, push parent + backend/storefront submodules, create org-scoped repos, recover from broken `gh auth` / SSH publickey errors, or fix missing workflow token scope. |
| `medusa-reference` | `medusa` | explicit | Medusa implementation guidance for backend and storefront work. Use when building or modifying Medusa workflows, subscribers, API routes, auth, data models, query logic, jobs, or storefront integrations. |
| `new-admin-via-api` | `medusa` | category | Create a Medusa v2 admin user against a running backend over HTTP, no CLI/SSH required. Two flows: (a) invite-accept for ADDITIONAL admins (needs an existing admin's session to mint the invite), (b) CLI fallback for the FIRST admin (no admin exists yet — Medusa v2 has no public POST /admin/users). Use when user says "create admin via API", "invite admin", "new admin on the live site", or supplies a backend URL + email + password and login is at /app/login. Medusa v2-only. |
| `new-user` | `medusa` | explicit | Create a new Medusa admin user via `npx medusa user -e <email> -p <password>`. Use when user says create admin, new admin user, /medusa-dev:user, or supplies an email + password pair for a Medusa backend. Medusa-only — NOT for general user creation. |
| `storefront-best-practices` | `medusa` | explicit | Use when working on ecommerce storefronts (Next.js, SvelteKit, React, Vue) — checkout, cart, payment flows, product pages, navigation, homepage, or ANY storefront component. Critical for adding checkout, implementing cart, integrating a Medusa backend, or building ecommerce functionality. |
| `woocommerce-to-medusa-import` | `medusa` | explicit | Build or run WooCommerce product importers into Medusa v2 backends. Use when importing WooCommerce products, variations, categories, images, prices, inventory, or metadata into Medusa, especially repos with apps/backend. Includes safe secret handling, dry-run/idempotent import rules, Medusa workflow usage, and verification steps. |
