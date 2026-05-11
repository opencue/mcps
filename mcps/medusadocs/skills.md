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
| `building-admin-dashboard-customizations` | `medusa` | prefix | Use when user says "Medusa admin", "admin widget", "custom admin page", "admin form", or plans/researches/implements Medusa Admin dashboard UI. Required for widgets, pages, forms, tables, data loading, and navigation. |
| `building-storefronts` | `medusa` | prefix | Use when user says "Medusa storefront", "call Medusa API", "SDK integration", "React Query", or plans/researches/implements storefront features. Required for storefront data fetching, mutations, cache handling, and Medusa API calls. |
| `building-with-medusa` | `medusa` | prefix | Use when user says "Medusa backend", "custom module", "API route", "workflow", "data model", or plans/researches/implements Medusa backend features. Required for modules, routes, workflows, links, and business logic. |
| `creating-internal-agents` | `medusa` | explicit | Use when user says "Medusa agent", "admin AI agent", "internal agent", "streamText", or builds an internal admin-facing AI agent in a Medusa project. Covers models, module service, runtime tools, NDJSON routes, and admin UI chat. NOT for buyer-side storefront chatbots. |
| `db-generate` | `medusa` | prefix | Use when user says "medusa db:generate", "generate migration", or "Medusa migration file" and needs Medusa migration generation guidance. Covers model changes, commands, review, and validation.argument-hint: <module-name> |
| `db-migrate` | `medusa` | prefix | Use when user says "medusa db:migrate", "run migrations", or "apply Medusa migration" and needs Medusa migration guidance. Covers environment checks, commands, rollback risk, and verification.allowed-tools: Bash(npx medusa db:migrate:*) |
| `gh-submodule-publish` | `medusa` | category | Use when user says "publish submodule", "GitHub submodule", or "Medusa submodule publish" and needs submodule publishing guidance. Covers repo state, commits, push, references, and validation. |
| `higgsfield-to-medusa-products` | `medusa` | category | Use when user says "Higgsfield to Medusa", "generate product photos", or "import AI product assets" and needs the Higgsfield-to-Medusa pipeline. Covers asset generation, product mapping, import, and validation.argument-hint: <shop> [<manifest.json>] |
| `medusa-reference` | `medusa` | explicit | Use when user says "Medusa workflow", "Medusa subscriber", "Medusa auth", "Medusa query", or builds/modifies Medusa API routes, data models, jobs, backend logic, storefront integrations, or implementation patterns. |
| `medusa-shop-setup` | `medusa` | category | Use when user says "new Medusa shop", "setup Medusa store", or "Medusa shop scaffold" and needs shop setup guidance. Covers base template, backend, storefront, envs, deployment, and checks. |
| `new-admin-via-api` | `medusa` | category | Use when user says "create Medusa admin", "new admin via API", or "add admin user" and needs API-based admin creation guidance. Covers auth, request shape, envs, validation, and risk.argument-hint: <backend-url> <email> <password> [<existing-admin-email> <existing-admin-password>] |
| `new-user` | `medusa` | explicit | Use when user says "new Medusa user", "create first admin", or "add user" and needs Medusa user creation guidance. Covers CLI/API options, credentials, validation, and handoff.argument-hint: <email> <password> |
| `provision-medusa-s3-bucket` | `medusa` | category | Use when user says "Medusa S3", "provision bucket", or "file storage bucket" and needs S3 bucket provisioning for Medusa. Covers envs, provider settings, access, and validation.argument-hint: <bucket-name> [<region=eu-central-1>] [<prefix=medusa/>] |
| `storefront-best-practices` | `medusa` | explicit | Use when user says "storefront best practices", "Medusa storefront", or "storefront architecture" and needs storefront guidance. Covers data fetching, UX, caching, errors, and validation. |
| `woocommerce-to-medusa-import` | `medusa` | explicit | Use when user says "WooCommerce import", "migrate products", or "Woo to Medusa" and needs WooCommerce-to-Medusa import guidance. Covers extraction, mapping, assets, import, and checks. |
