#!/usr/bin/env -S uv run -q --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.0.0",
#     "httpx>=0.27",
# ]
# ///
"""Marva Blog MCP server.

Stdio MCP that wraps the MARVA Home Medusa v2 admin blog API so Claude can
draft, list, update, publish, and revalidate posts on
https://admin.marvahome.com without leaving the conversation. Thumbnails
are produced upstream (Higgsfield MCP, S3, or any hosted URL) and attached
by URL via `marva_blog_set_thumbnail` — this server does not generate
images itself.

Authentication: Medusa v2 admin JWT. Provide either a pre-fetched
`MARVA_ADMIN_TOKEN` or admin `MARVA_ADMIN_EMAIL` / `MARVA_ADMIN_PASSWORD`
credentials; the server will exchange them via
POST /auth/user/emailpass and cache the JWT in-process for ~30 minutes.

Config (env):
    MARVA_BACKEND_URL      default https://admin.marvahome.com
    MARVA_ADMIN_EMAIL      admin login email (used if no MARVA_ADMIN_TOKEN)
    MARVA_ADMIN_PASSWORD   admin login password
    MARVA_ADMIN_TOKEN      optional pre-fetched JWT, bypasses login
    MARVA_PUBLISHABLE_KEY  optional, only used for /store/* reads

Tools:
    marva_blog_list                 — list posts (status=all|draft|published)
    marva_blog_get                  — fetch one post by slug
    marva_blog_create_draft         — POST action=create
    marva_blog_update               — POST action=update with patch
    marva_blog_set_thumbnail        — convenience: update thumbnail_url
    marva_blog_publish              — POST action=publish + revalidate
    marva_blog_unpublish            — POST action=unpublish + revalidate
    marva_blog_delete               — POST action=delete + revalidate
    marva_blog_revalidate           — manual cache bust
    marva_blog_validate_sections    — local section linter

Run: uv run ~/Documents/soul/mcps/mcps/marva-blog/server.py
Register in ~/.claude.json mcpServers as `marva-blog`.
"""
from __future__ import annotations

import os
import re
import time
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Config (read once at import time so the values survive across tool calls).
# ---------------------------------------------------------------------------

BACKEND_URL = os.environ.get(
    "MARVA_BACKEND_URL", "https://admin.marvahome.com"
).rstrip("/")
ADMIN_EMAIL = os.environ.get("MARVA_ADMIN_EMAIL", "").strip()
ADMIN_PASSWORD = os.environ.get("MARVA_ADMIN_PASSWORD", "").strip()
ADMIN_TOKEN_ENV = os.environ.get("MARVA_ADMIN_TOKEN", "").strip()
PUBLISHABLE_KEY = os.environ.get("MARVA_PUBLISHABLE_KEY", "").strip()

HTTP_TIMEOUT = 20.0
# Soft TTL on a fetched admin JWT. Medusa's default access token lifetime is
# longer than this; we re-login proactively to avoid in-flight expirations.
TOKEN_TTL_SECS = 30 * 60

_token_cache: dict[str, Any] = {"token": "", "fetched_at": 0.0}

mcp = FastMCP("marva-blog")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


class BlogError(RuntimeError):
    """Raised for any user-visible failure. The tool wrappers translate this
    into a structured `{ok: false, ...}` response so the MCP transport never
    sees an unhandled exception."""


async def _admin_token() -> str:
    """Return a valid admin JWT. Order:

    1. `MARVA_ADMIN_TOKEN` env var if set (never expires from our POV).
    2. Cached token from a prior `/auth/user/emailpass` login that's still
       within the soft TTL.
    3. Fresh login with `MARVA_ADMIN_EMAIL` / `MARVA_ADMIN_PASSWORD`.

    Raises BlogError with an actionable message if no auth path is viable.
    """
    if ADMIN_TOKEN_ENV:
        return ADMIN_TOKEN_ENV

    cached = _token_cache.get("token") or ""
    fetched_at = float(_token_cache.get("fetched_at") or 0.0)
    if cached and (time.time() - fetched_at) < TOKEN_TTL_SECS:
        return cached

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        raise BlogError(
            "No admin credentials configured. Set MARVA_ADMIN_TOKEN, or both "
            "MARVA_ADMIN_EMAIL and MARVA_ADMIN_PASSWORD."
        )

    url = f"{BACKEND_URL}/auth/user/emailpass"
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                url,
                json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
                headers={"content-type": "application/json"},
            )
    except httpx.HTTPError as e:
        raise BlogError(f"login transport error to {url}: {e}") from e

    if resp.status_code >= 400:
        body = (resp.text or "").strip()[:400]
        raise BlogError(
            f"admin login failed: HTTP {resp.status_code} from {url}: {body}"
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise BlogError(f"admin login returned non-JSON: {resp.text[:200]}") from e

    token = (data or {}).get("token") or ""
    if not token:
        raise BlogError(f"admin login returned no token: {data!r}")

    _token_cache["token"] = token
    _token_cache["fetched_at"] = time.time()
    return token


async def _admin_request(
    method: str,
    path: str,
    *,
    json_body: dict | None = None,
) -> dict:
    """Authenticated request against /admin/*. Returns parsed JSON. Raises
    BlogError with the upstream status + truncated body on non-2xx."""
    token = await _admin_token()
    url = f"{BACKEND_URL}{path}"
    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.request(
                method, url, headers=headers, json=json_body
            )
    except httpx.HTTPError as e:
        raise BlogError(f"transport error {method} {url}: {e}") from e

    if resp.status_code >= 400:
        body = (resp.text or "").strip()[:600]
        raise BlogError(
            f"upstream {method} {path} -> HTTP {resp.status_code}: {body}"
        )

    if not resp.content:
        return {}
    try:
        return resp.json()
    except ValueError as e:
        raise BlogError(
            f"upstream {method} {path} returned non-JSON: {resp.text[:200]}"
        ) from e


async def _store_request(path: str) -> dict:
    """Public /store/* GET. Sends MARVA_PUBLISHABLE_KEY if configured."""
    url = f"{BACKEND_URL}{path}"
    headers: dict[str, str] = {}
    if PUBLISHABLE_KEY:
        headers["x-publishable-api-key"] = PUBLISHABLE_KEY
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(url, headers=headers)
    except httpx.HTTPError as e:
        raise BlogError(f"transport error GET {url}: {e}") from e
    if resp.status_code >= 400:
        body = (resp.text or "").strip()[:600]
        raise BlogError(f"upstream GET {path} -> HTTP {resp.status_code}: {body}")
    try:
        return resp.json() if resp.content else {}
    except ValueError as e:
        raise BlogError(f"upstream GET {path} non-JSON: {resp.text[:200]}") from e


def _id_or_slug_body(slug_or_id: str, **rest: Any) -> dict:
    """Decide whether the supplied identifier is a Medusa-style internal id
    (anything starting with `bpost_`) or a slug, and place it on the right
    field of the request body. Extra fields are merged in."""
    body: dict[str, Any] = dict(rest)
    if not slug_or_id:
        raise BlogError("slug_or_id is required")
    if slug_or_id.startswith("bpost_") or slug_or_id.startswith("post_"):
        body["id"] = slug_or_id
    else:
        body["slug"] = slug_or_id
    return body


async def _revalidate(slugs: list[str]) -> dict:
    """POST /admin/blog/revalidate. Always returns a dict (empty on no-op)."""
    clean = [s for s in (slugs or []) if isinstance(s, str) and s]
    if not clean:
        return {"ok": True, "skipped": True, "reason": "no slugs"}
    return await _admin_request(
        "POST",
        "/admin/blog/revalidate",
        json_body={"slugs": clean},
    )


def _safe(coro_callable):
    """Decorator that turns BlogError + arbitrary exceptions into a structured
    `{ok: false, error, ...}` response so MCP tool calls never crash. The
    wrapped coroutine must return a dict-like payload on success."""

    async def wrapper(*args, **kwargs):
        try:
            result = await coro_callable(*args, **kwargs)
            return result
        except BlogError as e:
            return {"ok": False, "error": str(e)}
        except Exception as e:  # pragma: no cover - defensive
            return {
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }

    wrapper.__name__ = coro_callable.__name__
    wrapper.__doc__ = coro_callable.__doc__
    return wrapper


def _resolve_slug(slug_or_id: str, post: dict | None) -> str | None:
    """Pull a slug out of the upstream response (preferred) or fall back to
    whichever identifier the caller passed in if it already looks like a
    slug. Used to drive the post-mutation revalidate call."""
    if isinstance(post, dict):
        s = post.get("slug")
        if isinstance(s, str) and s:
            return s
    if slug_or_id and not (
        slug_or_id.startswith("bpost_") or slug_or_id.startswith("post_")
    ):
        return slug_or_id
    return None


# ---------------------------------------------------------------------------
# Tools — read
# ---------------------------------------------------------------------------


@mcp.tool()
@_safe
async def marva_blog_list(status: str = "all", limit: int = 50) -> list[dict]:
    """List Marva Home blog posts via the admin API.

    Args:
        status: "all" | "draft" | "published". Filtered client-side after
            the admin list returns (the upstream returns everything).
        limit: max rows to return after filtering (1-500).

    Returns: list of post DTOs (newest first per the admin endpoint).
    Each DTO has at least: id, slug, title, description, status,
    thumbnail_url, author_name, tags, sections, created_at, updated_at,
    published_at.
    """
    status_norm = (status or "all").lower().strip()
    if status_norm not in {"all", "draft", "published"}:
        raise BlogError(
            f"status must be 'all', 'draft', or 'published'; got '{status}'"
        )
    limit = max(1, min(500, int(limit)))

    payload = await _admin_request("GET", "/admin/blog/posts")
    posts = payload.get("posts") if isinstance(payload, dict) else None
    if not isinstance(posts, list):
        return []

    def _matches(p: dict) -> bool:
        if status_norm == "all":
            return True
        s = (p.get("status") or "").lower()
        if status_norm == "published":
            return s == "published" or bool(p.get("published_at"))
        # draft
        return s == "draft" or (not s and not p.get("published_at"))

    return [p for p in posts if isinstance(p, dict) and _matches(p)][:limit]


@mcp.tool()
@_safe
async def marva_blog_get(slug: str) -> dict:
    """Fetch one blog post by slug. Uses the admin list and filters locally
    so drafts are reachable too (the public /store endpoint only returns
    published posts).

    Args:
        slug: the post's url slug, e.g. "hello-world".
    """
    if not slug:
        raise BlogError("slug is required")
    payload = await _admin_request("GET", "/admin/blog/posts")
    posts = payload.get("posts") if isinstance(payload, dict) else None
    if isinstance(posts, list):
        for p in posts:
            if isinstance(p, dict) and p.get("slug") == slug:
                return p
    # Fallback to the public endpoint in case the slug is published but
    # somehow missing from the admin list response.
    try:
        store = await _store_request(f"/store/blog/posts/{slug}")
        post = store.get("post") if isinstance(store, dict) else None
        if isinstance(post, dict):
            return post
    except BlogError:
        pass
    raise BlogError(f"no post with slug '{slug}'")


# ---------------------------------------------------------------------------
# Tools — write
# ---------------------------------------------------------------------------


@mcp.tool()
@_safe
async def marva_blog_create_draft(
    slug: str,
    title: str,
    description: str,
    sections: list[dict],
    tags: list[str] | None = None,
    thumbnail_url: str | None = None,
    author_name: str = "Marva Home",
    author_role: str | None = None,
) -> dict:
    """Create a new blog post in draft status.

    Args:
        slug: kebab-case url slug, must be unique. Required.
        title: human-readable title. Required.
        description: short summary shown on listings. May be "" while still
            a draft; must be non-empty before publish.
        sections: list of {id, title, paragraphs, bullets?, code?} blocks.
            `id` must be kebab-case, each section needs >=1 paragraph.
            Run `marva_blog_validate_sections` first if unsure.
        tags: list of free-form tag strings.
        thumbnail_url: absolute https URL or site-relative "/uploads/..." path.
        author_name: defaults to "Marva Home".
        author_role: optional role line under the author name.

    Returns: `{post: {...full DTO...}}` on success.
    """
    if not slug or not title:
        raise BlogError("slug and title are required")

    post_body: dict[str, Any] = {
        "slug": slug,
        "title": title,
        "description": description or "",
        "author_name": author_name or "Marva Home",
        "tags": list(tags or []),
        "sections": list(sections or []),
    }
    if thumbnail_url is not None:
        post_body["thumbnail_url"] = thumbnail_url
    if author_role is not None:
        post_body["author_role"] = author_role

    return await _admin_request(
        "POST",
        "/admin/blog/posts",
        json_body={"action": "create", "post": post_body},
    )


@mcp.tool()
@_safe
async def marva_blog_update(slug_or_id: str, patch: dict) -> dict:
    """Update an existing blog post. Pass either the slug or the internal id.

    Args:
        slug_or_id: identifier of the post to update. IDs starting with
            "bpost_" or "post_" are routed as id; everything else as slug.
        patch: partial post object. Any of slug, title, description,
            thumbnail_url, author_name, author_role, author_avatar_url,
            tags, sections, metadata. Empty patch is rejected upstream.

    Returns: `{post: {...full DTO...}}` on success.
    """
    if not isinstance(patch, dict) or not patch:
        raise BlogError("patch must be a non-empty object")
    body = _id_or_slug_body(slug_or_id, action="update", patch=patch)
    return await _admin_request("POST", "/admin/blog/posts", json_body=body)


@mcp.tool()
@_safe
async def marva_blog_set_thumbnail(slug_or_id: str, thumbnail_url: str) -> dict:
    """Convenience wrapper around `marva_blog_update` that sets just the
    thumbnail. Accepts a full https URL or a site-relative "/uploads/..."
    path (matches the backend zod validator).

    Use this after generating an image with the Higgsfield MCP or uploading
    one to S3 — pass the resulting URL in.
    """
    if not thumbnail_url:
        raise BlogError("thumbnail_url is required")
    if not (
        thumbnail_url.startswith("/")
        or re.match(r"^https?://", thumbnail_url, re.IGNORECASE)
    ):
        raise BlogError(
            "thumbnail_url must start with http(s):// or be a site-relative "
            "path starting with '/'"
        )
    body = _id_or_slug_body(
        slug_or_id, action="update", patch={"thumbnail_url": thumbnail_url}
    )
    return await _admin_request("POST", "/admin/blog/posts", json_body=body)


@mcp.tool()
@_safe
async def marva_blog_publish(slug_or_id: str) -> dict:
    """Publish a blog post and bust the storefront cache. The post must have
    a non-empty description (enforced by the create/upsert workflow).

    Returns: `{post: {...DTO...}, revalidate: {...}}`.
    """
    body = _id_or_slug_body(slug_or_id, action="publish")
    result = await _admin_request("POST", "/admin/blog/posts", json_body=body)
    post = result.get("post") if isinstance(result, dict) else None
    slug = _resolve_slug(slug_or_id, post)
    revalidate = await _revalidate([slug] if slug else [])
    return {"post": post, "revalidate": revalidate}


@mcp.tool()
@_safe
async def marva_blog_unpublish(slug_or_id: str) -> dict:
    """Unpublish a blog post (returns it to draft status) and revalidate the
    storefront cache."""
    body = _id_or_slug_body(slug_or_id, action="unpublish")
    result = await _admin_request("POST", "/admin/blog/posts", json_body=body)
    post = result.get("post") if isinstance(result, dict) else None
    slug = _resolve_slug(slug_or_id, post)
    revalidate = await _revalidate([slug] if slug else [])
    return {"post": post, "revalidate": revalidate}


@mcp.tool()
@_safe
async def marva_blog_delete(slug_or_id: str) -> dict:
    """Permanently delete a blog post and revalidate the storefront."""
    # Capture the slug BEFORE deletion so we can still revalidate it after
    # the row is gone (the response post field may be null for deletes).
    slug_hint: str | None = None
    if not (
        slug_or_id.startswith("bpost_") or slug_or_id.startswith("post_")
    ):
        slug_hint = slug_or_id

    body = _id_or_slug_body(slug_or_id, action="delete")
    result = await _admin_request("POST", "/admin/blog/posts", json_body=body)
    post = result.get("post") if isinstance(result, dict) else None
    slug = _resolve_slug(slug_or_id, post) or slug_hint
    revalidate = await _revalidate([slug] if slug else [])
    return {"deleted": True, "post": post, "revalidate": revalidate}


@mcp.tool()
@_safe
async def marva_blog_revalidate(slugs: list[str] | None = None) -> dict:
    """Manually bust the storefront cache for one or more slugs. Pass an
    empty list (or omit `slugs`) to no-op safely.

    Returns the upstream `/admin/blog/revalidate` payload, typically
    `{ok: true, status: 200, ...}`.
    """
    return await _revalidate(list(slugs or []))


# ---------------------------------------------------------------------------
# Tools — local-only utility
# ---------------------------------------------------------------------------


_SECTION_ID_RE = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$|^[a-z]$")


@mcp.tool()
async def marva_blog_validate_sections(sections: list[dict]) -> dict:
    """Lint a sections array before posting it to the backend.

    Rules:
      * sections must be a non-empty list.
      * each section needs `id`, `title`, and at least one paragraph.
      * `id` must be kebab-case (a-z, 0-9, dashes).
      * paragraph entries, bullet entries, and `code` must be strings if set.

    Returns: `{ok: bool, issues: [str, ...], section_count: int}`.
    Does not call the backend.
    """
    issues: list[str] = []
    if not isinstance(sections, list) or not sections:
        return {"ok": False, "issues": ["sections must be a non-empty list"], "section_count": 0}

    seen_ids: set[str] = set()
    for i, sec in enumerate(sections):
        prefix = f"sections[{i}]"
        if not isinstance(sec, dict):
            issues.append(f"{prefix}: must be an object")
            continue

        sid = sec.get("id")
        if not isinstance(sid, str) or not sid:
            issues.append(f"{prefix}.id: required non-empty string")
        elif not _SECTION_ID_RE.match(sid):
            issues.append(
                f"{prefix}.id: '{sid}' must be kebab-case (a-z, 0-9, dashes)"
            )
        elif sid in seen_ids:
            issues.append(f"{prefix}.id: '{sid}' duplicates an earlier section")
        else:
            seen_ids.add(sid)

        title = sec.get("title")
        if not isinstance(title, str) or not title.strip():
            issues.append(f"{prefix}.title: required non-empty string")

        paragraphs = sec.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            issues.append(f"{prefix}.paragraphs: at least one paragraph required")
        else:
            for j, para in enumerate(paragraphs):
                if not isinstance(para, str):
                    issues.append(f"{prefix}.paragraphs[{j}]: must be a string")
                elif not para.strip():
                    issues.append(f"{prefix}.paragraphs[{j}]: empty string")

        bullets = sec.get("bullets")
        if bullets is not None:
            if not isinstance(bullets, list):
                issues.append(f"{prefix}.bullets: must be a list if set")
            else:
                for j, b in enumerate(bullets):
                    if not isinstance(b, str):
                        issues.append(f"{prefix}.bullets[{j}]: must be a string")

        code = sec.get("code")
        if code is not None and not isinstance(code, str):
            issues.append(f"{prefix}.code: must be a string if set")

    return {
        "ok": len(issues) == 0,
        "issues": issues,
        "section_count": len(sections),
    }


# ---------------------------------------------------------------------------
# Content Plan — helpers + tools
# ---------------------------------------------------------------------------

_PLAN_TONES: set[str] = {"explainer", "how-to", "listicle", "product"}
_PLAN_STATUSES: set[str] = {
    "queued",
    "drafting",
    "draft_ready",
    "published",
    "skipped",
}
_PLAN_DIFFICULTY: set[str] = {"low", "med", "high"}
_PLAN_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_iso_date(value: str, field: str = "planned_date") -> str:
    """Ensure `value` is a YYYY-MM-DD calendar date the backend will accept."""
    if not isinstance(value, str) or not _PLAN_DATE_RE.match(value):
        raise BlogError(f"{field} must be ISO 'YYYY-MM-DD'; got {value!r}")
    # Reject obvious month/day overflow (e.g. 2026-13-40).
    try:
        from datetime import date as _date

        y, m, d = (int(p) for p in value.split("-"))
        _date(y, m, d)
    except ValueError as e:
        raise BlogError(f"{field} is not a real date: {value} ({e})") from e
    return value


def _validate_tone(tone: str) -> str:
    if tone not in _PLAN_TONES:
        raise BlogError(
            f"tone must be one of {sorted(_PLAN_TONES)}; got {tone!r}"
        )
    return tone


def _validate_status(status: str) -> str:
    if status not in _PLAN_STATUSES:
        raise BlogError(
            f"status must be one of {sorted(_PLAN_STATUSES)}; got {status!r}"
        )
    return status


def _validate_difficulty(value: str) -> str:
    if value not in _PLAN_DIFFICULTY:
        raise BlogError(
            f"difficulty must be one of {sorted(_PLAN_DIFFICULTY)}; got {value!r}"
        )
    return value


@mcp.tool()
@_safe
async def marva_plan_list(
    date_from: str | None = None,
    date_to: str | None = None,
    status: str | None = None,
    tone: str | None = None,
) -> list[dict]:
    """List Content Plan articles in a date range, optionally filtered by status/tone.

    Use to inspect the editorial calendar before drafting. All filters are optional;
    omit them to fetch everything the backend returns.
    """
    params: list[str] = []
    if date_from is not None:
        params.append(f"from={_validate_iso_date(date_from, 'date_from')}")
    if date_to is not None:
        params.append(f"to={_validate_iso_date(date_to, 'date_to')}")
    if status is not None:
        params.append(f"status={_validate_status(status)}")
    if tone is not None:
        params.append(f"tone={_validate_tone(tone)}")

    qs = ("?" + "&".join(params)) if params else ""
    payload = await _admin_request("GET", f"/admin/content-plan/articles{qs}")
    if isinstance(payload, dict):
        articles = payload.get("articles")
        if isinstance(articles, list):
            return [a for a in articles if isinstance(a, dict)]
    return []


@mcp.tool()
@_safe
async def marva_plan_get(id: str) -> dict:
    """Fetch one Content Plan article by id.

    Use after `marva_plan_list` to inspect a specific slot before promoting/editing.
    """
    if not id:
        raise BlogError("id is required")
    payload = await _admin_request("GET", f"/admin/content-plan/articles?id={id}")
    if isinstance(payload, dict):
        articles = payload.get("articles")
        if isinstance(articles, list):
            for a in articles:
                if isinstance(a, dict) and a.get("id") == id:
                    return a
    raise BlogError(f"no planned article with id '{id}'")


@mcp.tool()
@_safe
async def marva_plan_create(
    planned_date: str,
    title: str,
    tone: str,
    brief: str | None = None,
    volume: int | None = None,
    difficulty: str | None = None,
) -> dict:
    """Create a new Content Plan slot for a future article.

    Use when scheduling a new article on the editorial calendar before drafting.
    `planned_date` is ISO `YYYY-MM-DD`; `tone` must match the plan vocabulary.
    """
    if not title:
        raise BlogError("title is required")
    article: dict[str, Any] = {
        "planned_date": _validate_iso_date(planned_date),
        "title": title,
        "tone": _validate_tone(tone),
    }
    if brief is not None:
        article["brief"] = brief
    if volume is not None:
        article["volume"] = int(volume)
    if difficulty is not None:
        article["difficulty"] = _validate_difficulty(difficulty)
    return await _admin_request(
        "POST",
        "/admin/content-plan/articles",
        json_body={"action": "create", "article": article},
    )


@mcp.tool()
@_safe
async def marva_plan_update(id: str, patch: dict) -> dict:
    """Update a Content Plan slot with a partial patch (title/tone/brief/status/etc).

    Use to retitle, reschedule, change tone, or move a slot through its status
    lifecycle. Validates `tone`, `status`, `difficulty`, and `planned_date` shape.
    """
    if not id:
        raise BlogError("id is required")
    if not isinstance(patch, dict) or not patch:
        raise BlogError("patch must be a non-empty object")

    normalized: dict[str, Any] = {}
    for key, value in patch.items():
        if value is None:
            normalized[key] = None
            continue
        if key == "tone":
            normalized[key] = _validate_tone(value)
        elif key == "status":
            normalized[key] = _validate_status(value)
        elif key == "difficulty":
            normalized[key] = _validate_difficulty(value)
        elif key == "planned_date":
            normalized[key] = _validate_iso_date(value)
        elif key == "volume":
            normalized[key] = int(value)
        else:
            normalized[key] = value
    return await _admin_request(
        "POST",
        "/admin/content-plan/articles",
        json_body={"action": "update", "id": id, "patch": normalized},
    )


@mcp.tool()
@_safe
async def marva_plan_delete(id: str) -> dict:
    """Delete a Content Plan slot (does NOT delete any promoted BlogPost draft).

    Use to cancel a calendar entry that won't be written. To remove a published
    article instead, use `marva_blog_delete` on the resulting post.
    """
    if not id:
        raise BlogError("id is required")
    return await _admin_request(
        "POST",
        "/admin/content-plan/articles",
        json_body={"action": "delete", "id": id},
    )


@mcp.tool()
@_safe
async def marva_plan_promote(
    id: str,
    sections: list[dict] | None = None,
    thumbnail_url: str | None = None,
    publish: bool = False,
) -> dict:
    """Promote a plan slot to a real BlogPost draft (optionally publishing it).

    Use at the end of drafting: the backend creates a BlogPost from the plan and
    links it back. With `publish=True`, also publishes the resulting post and
    revalidates the storefront cache.
    """
    if not id:
        raise BlogError("id is required")
    body: dict[str, Any] = {}
    if sections is not None:
        body["sections"] = list(sections)
    if thumbnail_url is not None:
        body["thumbnail_url"] = thumbnail_url
    # Let the backend decide whether to publish itself if it supports the flag,
    # but we still do the storefront-side publish + revalidate below for safety.
    if publish:
        body["publish"] = True

    promote_result = await _admin_request(
        "POST",
        f"/admin/content-plan/articles/{id}/promote",
        json_body=body or None,
    )

    post = (
        promote_result.get("post") if isinstance(promote_result, dict) else None
    )
    plan = (
        promote_result.get("plan") if isinstance(promote_result, dict) else None
    )

    publish_result: dict | None = None
    revalidate_result: dict | None = None
    if publish and isinstance(post, dict):
        slug_or_id = post.get("slug") or post.get("id")
        post_status = (post.get("status") or "").lower()
        if post_status != "published" and slug_or_id:
            pub_body = _id_or_slug_body(str(slug_or_id), action="publish")
            publish_result = await _admin_request(
                "POST", "/admin/blog/posts", json_body=pub_body
            )
            pub_post = (
                publish_result.get("post")
                if isinstance(publish_result, dict)
                else None
            )
            if isinstance(pub_post, dict):
                post = pub_post
        slug = _resolve_slug(str(slug_or_id or ""), post)
        revalidate_result = await _revalidate([slug] if slug else [])

    return {
        "plan": plan,
        "post": post,
        "publish": publish_result,
        "revalidate": revalidate_result,
    }


if __name__ == "__main__":
    mcp.run()
