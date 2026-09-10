# Lobby

**Lobby** is a minimal, self-hosted app launcher — an iOS-homescreen-style
grid of links to your own apps and services, behind a login. It's a
lightweight alternative to dashboards like Homer, Homarr, Heimdall, or Dashy
for people who just want a fast, private launchpad for their homelab or
self-hosted stack. Add it to your phone's homescreen for a one-tap dashboard
to Plex, Jellyfin, Nextcloud, Dokploy, Portainer, n8n, or anything else you
run.

![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-3-black)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Zero-config first run** — visit the site, create your admin login at
  `/setup`, done. No env vars required to get started.
- **Multi-user** — add or remove logins from `/manage`, no config file
  editing or redeploys.
- **App grid** — add, edit, and delete launcher tiles from `/manage`, with
  live icon search powered by [selfh.st/icons](https://selfh.st/icons/) (or
  just paste an emoji or image URL).
- **Persistent data** — apps and users are stored in a Docker volume, so
  edits survive redeploys.
- **PWA-ready** — installs to your phone's homescreen like a native app.
- **Tiny footprint** — one Flask app, one Docker image, no database.

## Quick start

```bash
git clone https://github.com/ardavannafezi/lobby.git
cd lobby
docker compose up -d
```

Visit `http://localhost:8000`, create your admin account at `/setup`, and
add it to your phone's homescreen.

Go to `/manage` to add, edit, or delete apps and users. Apps and users are
stored in the `lobby_data` volume (`apps.json` in the repo is only the seed
for a first run).

### Optional configuration

Copy `.env.example` to `.env` if you want to pin a `SECRET_KEY` (e.g. for a
multi-instance deployment); otherwise one is generated and persisted
automatically on first run.

## Deploying

Any Docker host works. On [Dokploy](https://dokploy.com), Coolify,
Portainer, or a plain VPS: point a new application at this repo (or the
prebuilt image) and assign a domain — no required env vars.

## Tech stack

Flask, Flask-Login, Tailwind (CDN), and a JSON file for storage. No
database, no build step, no JavaScript framework.

## License

MIT
