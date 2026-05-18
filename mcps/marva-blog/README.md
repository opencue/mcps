# Marva Blog MCP

Source URL: local

Install command:

```sh
~/.local/bin/uv run --script /home/deadpool/Documents/soul/mcps/mcps/marva-blog/server.py
```

Expected command/type:

```text
command: /home/deadpool/.local/bin/uv
args:
  - run
  - --quiet
  - --script
  - /home/deadpool/Documents/soul/mcps/mcps/marva-blog/server.py
type: stdio
```

Required env vars:

```text
MARVA_BACKEND_URL=https://admin.marvahome.com
MARVA_ADMIN_EMAIL=...
MARVA_ADMIN_PASSWORD=...
# OR pre-fetched JWT (skips emailpass login):
MARVA_ADMIN_TOKEN=...
# Optional, only for /store/* reads:
MARVA_PUBLISHABLE_KEY=...
```

Related skills:

```text
marva-blog-author
```

## Tools

| Tool | Purpose |
| --- | --- |
| `marva_blog_list` | List posts; filter by status (`all`, `draft`, `published`). |
| `marva_blog_get` | Fetch one post by slug (admin list, falls back to /store). |
| `marva_blog_create_draft` | Create a draft post with sections, tags, optional thumbnail. |
| `marva_blog_update` | Update a post by slug or id with a partial patch. |
| `marva_blog_set_thumbnail` | Convenience: set just `thumbnail_url`. |
| `marva_blog_publish` | Publish a post and revalidate the storefront cache. |
| `marva_blog_unpublish` | Move a post back to draft and revalidate. |
| `marva_blog_delete` | Delete a post and revalidate. |
| `marva_blog_revalidate` | Manual cache bust for one or more slugs. |
| `marva_blog_validate_sections` | Local linter for the sections array shape. |

## Quick start

```text
1. marva_blog_validate_sections(sections=[...])         # sanity check
2. marva_blog_create_draft(slug="hello-marva",
       title="Hello Marva", description="...", sections=[...])
3. (optional) generate an image with the Higgsfield MCP, upload to S3
4. marva_blog_set_thumbnail("hello-marva", "https://cdn.../hero.jpg")
5. marva_blog_publish("hello-marva")
```

`marva_blog_publish` also POSTs to `/admin/blog/revalidate` so the public
storefront at `https://marvahome.com/blog/<slug>` picks up the change
within seconds.

## Quick health check

```sh
python3 -c 'import httpx, sys; r=httpx.get("https://admin.marvahome.com/health", timeout=5); print(r.status_code); sys.exit(0 if r.status_code < 500 else 1)'
```
