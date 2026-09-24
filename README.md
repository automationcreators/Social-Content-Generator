# Social Content Generator

CLI and local UI that draft social posts from your own project notes, RSS items, and hook frameworks. Output lands in `generated_content/` and, if you configure Google OAuth, in a Google Sheet.

This checkout is a **demo snapshot**. It does not include API keys, OAuth tokens, or a ContentGen database. You can read the generators and the sample posts without credentials. Live generation, Sheets sync, and Drive upload stay off until you supply your own env vars.

## What it does

1. Reads recent items from a local ContentGen SQLite database (`CONTENTGEN_DB`).
2. Scores them and drafts angles (professional, contrarian, balanced).
3. Mixes in examples from a local projects directory (`ACTIVE_PROJECTS_DIR`).
4. Writes posts, threads, and pillar scripts under `generated_content/` and `pillar_scripts/`.
5. Optionally appends rows to Google Sheets or uploads scripts to Drive.

Sample posts already in `generated_content/` are static. They are not a live feed.

## Demo vs production

| | Demo (this repo) | Production |
| --- | --- | --- |
| Sample posts | Read the JSON/CSV in `generated_content/` | Generate new posts daily |
| API keys | None committed | Your Gemini key in `.env` |
| Google OAuth | Not included | Client JSON + `token.pickle` outside the repo |
| ContentGen DB | Not included | Your own RSS database |
| Sheets / Drive | Placeholders only | Your spreadsheet and folder |
| Scheduling | Script exists; cron is opt-in | Your machine, your cron |

Do not point this at customer lists, private inboxes, or someone else's Drive folder. Generated copy in this repo has had personal filesystem paths, private Drive folder ids, and named individuals from a research dataset replaced with placeholders. Git history may still contain the old values. See the pull request notes before treating history as clean.

## Run it

Python 3.9+. Node 18+ only if you want the Next.js UI.

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Static check of the sample library (no API key)
python3 -c "import json; d=json.load(open('generated_content/social-content-all-100.json')); print(len(d['posts']), 'posts')"

# Daily draft. Fails closed if CONTENTGEN_DB is missing.
python3 automation/daily_content_generator.py --mode balanced
```

Load env vars into the shell before the Python process (`set -a && source .env && set +a`, or your own runner). The scripts read the process environment. They do not load `.env` automatically.

### Environment variables

Copy `.env.example`. Every value below is a placeholder.

| Variable | Used by | Required for |
| --- | --- | --- |
| `SCG_WORKSPACE_ROOT` | agent framework, Gemini script generator | Anything that looks up sibling projects |
| `CONTENTGEN_DB` | `scouts/rss_content_scout.py` | RSS-based drafts |
| `ACTIVE_PROJECTS_DIR` | project collector, weekly progress agent | Example mining |
| `GOOGLE_API_KEY` | `pillar_scripts/unified_gemini_youtube_generator.py` | Live Gemini calls |
| `GDRIVE_FOLDER_ID` | Drive upload scripts | Uploads |
| `GOOGLE_CREDENTIALS_DIR` | Drive OAuth | Where `google-drive-credentials.json` and `token.pickle` live |
| `NEXT_PUBLIC_API_URL` | `frontend/next.config.js` | UI talking to the API |

OAuth setup, if you need Sheets or Drive:

1. In Google Cloud Console, create an OAuth client (Desktop) for the Drive and Sheets APIs you actually use.
2. Save the client JSON as `$GOOGLE_CREDENTIALS_DIR/google-drive-credentials.json`.
3. Run an upload or sync script once and complete the browser consent flow. The token is written next to that JSON as `token.pickle`.
4. Do not commit either file. `.gitignore` ignores `*.pickle`, `client_secret*.json`, and `google-drive-credentials.json`.

### UI

```bash
cp frontend/.env.example frontend/.env.local
cd frontend && npm install && npm run dev
```

In another shell, from the repo root:

```bash
pip install -r backend/requirements.txt
cd backend && python3 main.py
```

UI: http://localhost:3000. API: http://localhost:8000. The UI calls Gemini and Drive only when `GOOGLE_API_KEY` and OAuth files exist.

### Daily cron

`automation/setup_daily_automation.sh` installs a 9:00 local cron entry for this clone. It uses `SCG_DIR` (default: the repo root) and `PYTHON_BIN` (default: `python3`). It does not embed a home-directory path or a Homebrew Python path.

## Layout

```
automation/     daily generator and cron helper
backend/        FastAPI used by the UI
config/         frameworks and a redacted project snapshot
frontend/       Next.js chat UI
generated_content/  sample posts (static)
generators/     angle, pillar, and orchestration scripts
pillar_scripts/ YouTube script generators and Drive upload
scouts/         RSS and project scanners
sync/           Google Sheets helpers (need local OAuth)
```

Sheets sync still expects a local `google_token.pickle` and a results JSON that contains your spreadsheet id. Neither is in this repo.

## Security

- No API keys, OAuth tokens, or private keys are committed in the current tree.
- `.env.example` and `frontend/.env.example` are placeholders. Real `.env` files are gitignored.
- Private Google Drive folder ids that used to be hardcoded are `REDACTED_DRIVE_FOLDER_ID` in docs and read from `GDRIVE_FOLDER_ID` in code.
- History was not rewritten. If a folder was shared by link, unshare it and create a new folder. Rotate any credential that ever lived in a file that was pushed, even if it is gone from the latest commit.

## Not in this demo

- A funded Gemini or OpenAI account
- Google OAuth consent for a public deploy
- The ContentGen database and Personal-OS agent directories
- Hosted scheduling, auth, or a multi-tenant product path

Those are the blockers between "safe to read and demo from samples" and "safe to run as a paid product."
