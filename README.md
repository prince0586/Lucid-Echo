# Lucid Echo - The Offline Dream Interpreter

Lucid Echo is an offline agent powered by GPT-OSS-20B that interprets dreams, retells them as myths, and tracks symbolic patterns over time.

## Features
- Dream journaling with local encrypted storage
- Symbolic interpretation using archetypes
- Creative retelling of dreams (myths/poems)
- Offline-first, no internet required

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run API server:
   ```bash
   uvicorn app:app --reload
   ```
3. Access endpoints:
   - POST `/interpret` → submit a dream
   - GET `/history` → retrieve dream history

## Integration
- `gpt_oss_wrapper.py` is a placeholder for integrating GPT-OSS-20B model locally.
- Extend `archetypes.py` and `personas.py` for richer interpretations.

## License
MIT License


## Frontend
A minimal React + Tailwind frontend is included in `frontend/`. Open `frontend/index.html` in a browser configured to proxy requests to the backend (or serve via a simple static server).

## CI / Docker Image Badge

GitHub Actions will build and publish a Docker image to GitHub Container Registry (GHCR) on pushes to `main`.
You can add a badge after the workflow runs; an example badge (replace `YOURUSER` and `REPO`):

```
![CI](https://github.com/YOURUSER/YOURREPO/actions/workflows/docker-publish.yml/badge.svg)
```

And a link to the container (replace `YOURUSER`):

```
https://ghcr.io/YOURUSER/lucid-echo
```

## Creating a Personal Access Token (PAT) for GHCR (optional)

If your repository or organization policies prevent the `GITHUB_TOKEN` from publishing packages, create a PAT and add it as a secret named `GHCR_PAT` in your repository settings.

1. Go to https://github.com/settings/tokens -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token.
2. Select an expiration (or no expiration for convenience).
3. Under scopes, check **write:packages** and **read:packages** (and `repo` if you will push code from scripts).
4. Generate the token and copy it.
5. In your GitHub repo, go to **Settings → Secrets and variables → Actions → New repository secret**.
6. Name it `GHCR_PAT` and paste the token value.
7. The workflow will now use `GHCR_PAT` preferentially; if it's not present it falls back to `GITHUB_TOKEN`.
