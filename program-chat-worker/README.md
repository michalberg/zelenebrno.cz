# Program chat worker

Small Cloudflare Worker behind the "Chatujte s chatbotem o programu" button on
`/program`. Receives a question, answers it with Claude using the full text
of `program_final.md` as grounding context (prompt-cached so repeat requests
are cheap and fast), and logs every question + answer to Cloudflare KV.

The site itself stays static on GitHub Pages — this worker is a separate
deploy, called from the browser exactly like the donate form already calls
`api.dary.zeleni.cz`.

## One-time setup

You'll need a [Cloudflare account](https://dash.cloudflare.com/sign-up) (free
tier is enough) and your Anthropic API key.

```bash
cd program-chat-worker
npm install

# Log in to Cloudflare (opens a browser window)
npx wrangler login

# Create the KV namespace used for logging + rate-limiting
npx wrangler kv namespace create CHAT_LOG
# ⤷ copy the "id" it prints, paste it into wrangler.toml
#   replacing REPLACE_WITH_KV_NAMESPACE_ID

# Set your secrets (you'll be prompted to paste the value — it's not stored
# in any file or shown in your terminal history)
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put ADMIN_TOKEN   # invent any password, used to view logs
```

## Deploy

```bash
npm run deploy
```

This prints a URL like `https://zb-program-chat.<your-subdomain>.workers.dev`.
Paste that into `PROGRAM_CHAT_ENDPOINT` in
`site/wp-content/themes/zeleni-new/assets/js/program-chat.js`, then rebuild
and redeploy the site as usual.

If you'd rather have it on your own domain (e.g.
`chat.zelenebrno.cz`), add a route/custom domain for the worker in the
Cloudflare dashboard (Workers & Pages → zb-program-chat → Settings →
Domains & Routes) — no code change needed, just update the endpoint URL in
`program-chat.js` to match.

## Updating the program text

The worker bundles `program_final.md` as a text module, copied in at build
time. After editing `docs/scripts/data/program_final.md`, just redeploy:

```bash
npm run deploy   # re-syncs the file automatically, then deploys
```

## Reading the logs

```bash
curl -H "Authorization: Bearer <your ADMIN_TOKEN>" \
  "https://<your-worker-url>/admin/logs?limit=100"
```

Returns the most recent Q&A pairs as JSON (question, answer, timestamp).
Logs are kept for 180 days. No IP addresses or other identifying
information are stored — only the question, the answer, and when it was
asked. (IPs are used transiently for rate-limiting — 6 questions/minute per
visitor — but that key expires after 60 seconds and is never written to the
log.)

## Cost

Each question costs a small fraction of a cent — Haiku is cheap, and prompt
caching means the ~55k-token program text is only billed at full price on
the first request each hour; after that, cached reads are ~10% of the
normal input price. Cloudflare Workers' free tier (100k requests/day) and KV
free tier will comfortably cover a campaign site's traffic.
