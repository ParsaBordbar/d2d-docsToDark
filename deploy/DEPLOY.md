# Deploying D2D

Two free targets: the API on **Hugging Face Spaces** (Docker), the client on
**Cloudflare Pages**. They talk over CORS, so deploy the API first, then point
the client at it and lock CORS back down.

---

## Phase 3 — API on Hugging Face Spaces

HF Spaces build the repo-root `Dockerfile` directly. No card required.

### 1. Create the Space
- New Space → SDK: **Docker** → **Blank** template → name e.g. `d2d-api`.
- This gives you a git repo at `https://huggingface.co/spaces/<user>/d2d-api`.

### 2. Push this project into it
HF reads config from the front matter of the Space's **root `README.md`**, so
that block must sit at the top of the root README in the Space repo. Copy the
front matter from `deploy/huggingface/README.md` there (`app_port: 1313` is the
important line — it maps the Space's public URL to our port).

```bash
git remote add space https://huggingface.co/spaces/<user>/d2d-api
git push space refactor/package-structure:main
```
(or merge to `main` first and push `main:main`.)

### 3. Set Space variables (Settings → Variables and secrets)
| var | value | why |
|---|---|---|
| `UPLOAD_DIR` | `/tmp/uploads` | `/app` may be read-only on HF; `/tmp` is writable |
| `ALLOWED_ORIGINS` | `https://<your-pages-domain>` | lock CORS to the client (set after Phase 4) |
| `FILE_MAX_AGE_SECONDS` | `1800` | optional — trim disk on the ephemeral Space |

The Space rebuilds on push. When it's green, the API is at
`https://<user>-d2d-api.hf.space` — check `/` and `/docs`.

> Note: free Spaces sleep after inactivity and the first request cold-starts.
> Uploaded/converted files are ephemeral (cleanup loop + no persistent disk).

---

## Phase 4 — Client on Cloudflare Pages

### 1. Point the client at the API
`client/.env` (build-time):
```
VITE_API_BASE_URL=https://<user>-d2d-api.hf.space
```

### 2. Cloudflare Pages project
- Connect the GitHub repo → set **root directory** to `client`.
- Build command: `npm run build` · Output dir: `dist`.
- Add env var `VITE_API_BASE_URL` = the Space URL (same as above).
  `client/.env` is gitignored, so this **must** be set in Pages → Settings →
  Variables; otherwise the bundle falls back to `http://localhost:1313`.

`client/wrangler.jsonc` pins `pages_build_output_dir` to `dist`, so Pages
serves the built bundle even if the dashboard output dir is wrong. If the site
loads as a blank page and `/src/main.tsx` or `/package.json` return 200, the
raw source tree was published: the build command was empty or the root
directory was not `client`. Fix the settings and **Retry deployment**.

### 3. Close the CORS loop
Once the Pages URL exists (`https://<proj>.pages.dev`), set the Space's
`ALLOWED_ORIGINS` to exactly that origin and let it rebuild. Confirm an upload
works end to end from the deployed client.
