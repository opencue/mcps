# financial-datasets skills

Market & company financial data for the `finance` profile. No related
`resources/skills` entries — this MCP is the data source itself.

MCP source: [https://github.com/financial-datasets/mcp-server](https://github.com/financial-datasets/mcp-server)

Homepage: [https://www.financialdatasets.ai](https://www.financialdatasets.ai)

Package: `git clone (uv run server.py)`

Install: `git clone https://github.com/financial-datasets/mcp-server && uv venv && uv add "mcp[cli]" httpx`

Expected type: `stdio`

Health command: `uv --directory <clone-dir> run server.py --help`

Owners: `financial-datasets`

Agent surfaces: `claude-code`

Requires env: `FINANCIAL_DATASETS_API_KEY` (get a key at financialdatasets.ai)

## Tools exposed (10)

| Tool | Description |
| --- | --- |
| Income statements | Retrieve company income statements (period + currency aware) |
| Balance sheets | Retrieve company balance sheets |
| Cash flow statements | Retrieve company cash flow statements |
| Current stock price | Latest quote for a ticker |
| Historical stock prices | Price history over a date range |
| Company news | Recent news articles for a ticker |
| Crypto ticker availability | Which crypto tickers are supported |
| Current crypto price | Latest quote for a crypto pair |
| Historical crypto prices | Crypto price history over a range |
| (financials helpers) | Period/segment helpers around the statements above |
