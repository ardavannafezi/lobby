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
2. Edit `apps.json` with your own apps:
   ```json
   [{ "name": "My App", "url": "https://myapp.example.com", "icon": "🚀" }]
   ```
3. Run:
   ```
   docker compose up -d
   ```
4. Visit `http://localhost:8000`, log in, add to your phone's homescreen.

## Deploying

Any Docker host works. On [Dokploy](https://dokploy.com), point a new
application at this repo, set the env vars above, and assign a domain.

## License

MIT
