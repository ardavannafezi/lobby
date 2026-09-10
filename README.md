# Lobby

Minimal self-hosted app launcher — an iOS-homescreen-style grid of links to
your own apps, behind a login. Add it to your phone's homescreen for a
one-tap dashboard.

## Setup

1. Copy `.env.example` to `.env` and fill in:
   - `LOBBY_USERNAME` — your login username
   - `LOBBY_PASSWORD_HASH` — generate with:
     ```
     python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('yourpassword'))"
     ```
   - `SECRET_KEY` — generate with `openssl rand -hex 32`
2. Run:
   ```
   docker compose up -d
   ```
3. Visit `http://localhost:8000`, log in, add to your phone's homescreen.
4. Go to `/manage` to add, edit, or delete apps — search
   [selfh.st/icons](https://selfh.st/icons/) right in the icon field, or type
   any emoji or image URL. Apps are stored in the `lobby_data` volume, so
   edits persist across redeploys (`apps.json` in the repo is only the seed
   for a first run).

## Deploying

Any Docker host works. On [Dokploy](https://dokploy.com), point a new
application at this repo, set the env vars above, and assign a domain.

## License

MIT
