# Higgsfield MCP

Source URL: https://mcp.higgsfield.ai/mcp

Install command:

```sh
# hosted MCP endpoint; no local package install required
```

Expected command/type:

```text
url: https://mcp.higgsfield.ai/mcp
type: hosted
```

Required env vars:

```text
none tracked here
```

Related skills:

```text
brandkit
higgsfield-*
imagegen-frontend-mobile
imagegen-frontend-web
```

Quick health check:

```sh
python3 -c 'from urllib.parse import urlparse; u=urlparse("https://mcp.higgsfield.ai/mcp"); raise SystemExit(0 if u.scheme and u.netloc else 1)'
```
