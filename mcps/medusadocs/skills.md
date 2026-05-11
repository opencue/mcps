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
| `db-generate` | `medusa` | prefix | Generate database migrations for a Medusa module via `npx medusa db:generate <module-name>`. Use when user says /medusa-dev:db-generate, generate migrations for module X, or modifies a Medusa module data model and needs migration files. Pair with /db-migrate to apply. |
| `db-migrate` | `medusa` | prefix | Apply pending Medusa database migrations via `npx medusa db:migrate`. Use when user says /medusa-dev:db-migrate, run migrations, apply pending migrations, or after running /db-generate to bring the database up to date. Reports applied count plus any errors. |
| `gh-submodule-publish` | `medusa` | category | Create missing GitHub repos and push a parent repo that tracks app repos as Git submodules. Use when user asks to publish locally-initialized repos, push parent + backend/storefront submodules, create org-scoped repos, recover from broken `gh auth` / SSH publickey errors, or fix missing workflow token scope. |
| `higgsfield-to-medusa-products` | `medusa` | category | End-to-end product imagery pipeline for Medusa v2 shops. Generates product shots via Higgsfield (`higgsfield product-photoshoot create`), uploads them to the shop's S3 bucket on a public-read prefix, then patches the matching Medusa products via `POST /admin/products/{id}` to set thumbnail + images. Use when user says "generate product images", "refresh product photos", "shop képeket generálni", "Higgsfield images to Medusa", or supplies a list of product slugs/IDs and prompts. Reads backend URL + secret + AWS creds from a per-shop config file (or a future recodee bouncer MCP), never hardcodes them. Idempotent — re-running overwrites the same S3 keys + product fields. |
| `medusa-reference` | `medusa` | explicit | Use when user says "Medusa workflow", "Medusa subscriber", "Medusa auth", "Medusa query", or builds/modifies Medusa API routes, data models, jobs, backend logic, storefront integrations, or implementation patterns. |
| `medusa-shop-setup` | `medusa` | category | Use when creating a new Medusa webshop from medusa-shops/base-template, generating backend/storefront env files from a domain, preparing Coolify backend deployment, configuring Hostinger hosting/DNS, creating the per-shop Postgres schema, or making a domain-to-shop setup checklist. Triggers include "new webshop", "create webshop", "base-template env", "configure envs for a site", "Coolify + Hostinger Medusa shop", and "domain address then setup .env". |
| `new-admin-via-api` | `medusa` | category | Create a Medusa v2 admin user against a running backend over HTTP, no CLI/SSH required. Two flows: (a) invite-accept for ADDITIONAL admins (needs an existing admin's session to mint the invite), (b) CLI fallback for the FIRST admin (no admin exists yet — Medusa v2 has no public POST /admin/users). Use when user says "create admin via API", "invite admin", "new admin on the live site", or supplies a backend URL + email + password and login is at /app/login. Medusa v2-only. |
| `new-user` | `medusa` | explicit | Create a new Medusa admin user via `npx medusa user -e <email> -p <password>`. Use when user says create admin, new admin user, /medusa-dev:user, or supplies an email + password pair for a Medusa backend. Medusa-only — NOT for general user creation. |
| `provision-medusa-s3-bucket` | `medusa` | category | Create and configure an AWS S3 bucket for a Medusa v2 backend in one shot. Sets up: bucket creation in a region, public-read bucket policy scoped to a product-images prefix, CORS for admin uploads, versioning, server-side encryption (SSE-S3), and lifecycle to clean up incomplete multipart uploads. Outputs the env var block ready to paste into `~/.config/woocommerce-medusa-import/env` AND the env vars to set in Coolify so the running Medusa file provider switches off local-storage to S3. Use when user says "create medusa bucket", "provision s3 for medusa", "new shop bucket", or supplies a shop name + AWS region. Requires `aws` CLI configured (or `AWS_ACCESS_KEY_ID`+`AWS_SECRET_ACCESS_KEY` in env). |
| `storefront-best-practices` | `medusa` | explicit | Use when working on ecommerce storefronts (Next.js, SvelteKit, React, Vue) — checkout, cart, payment flows, product pages, navigation, homepage, or ANY storefront component. Critical for adding checkout, implementing cart, integrating a Medusa backend, or building ecommerce functionality. |
| `woocommerce-to-medusa-import` | `medusa` | explicit | Build or run WooCommerce product importers into Medusa v2 backends. Use when importing WooCommerce products, variations, categories, images, prices, inventory, or metadata into Medusa, especially repos with apps/backend. Includes safe secret handling, dry-run/idempotent import rules, Medusa workflow usage, and verification steps. |
