import json
import os
import secrets
import shutil
from datetime import timedelta

from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=365)

login_manager = LoginManager(app)
login_manager.login_view = "login"

USERNAME = os.environ["LOBBY_USERNAME"]
PASSWORD_HASH = os.environ["LOBBY_PASSWORD_HASH"]

DATA_FILE = os.environ.get("LOBBY_DATA_FILE", os.path.join(app.root_path, "data", "apps.json"))
SEED_FILE = os.path.join(app.root_path, "apps.json")


def load_apps():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        shutil.copy(SEED_FILE, DATA_FILE)
    with open(DATA_FILE) as f:
        return json.load(f)


def save_apps(apps):
    with open(DATA_FILE, "w") as f:
        json.dump(apps, f, indent=2)


class User(UserMixin):
    id = USERNAME


@login_manager.user_loader
def load_user(user_id):
    return User() if user_id == USERNAME else None


@app.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.post("/login")
def login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
        login_user(User(), remember=True)
        return redirect(url_for("index"))
    return render_template("login.html", error="Invalid credentials"), 401


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.get("/")
@login_required
def index():
    return render_template("index.html", apps=load_apps())


@app.get("/manage")
@login_required
def manage():
    return render_template("manage.html", apps=load_apps())


@app.post("/manage/add")
@login_required
def manage_add():
    apps = load_apps()
    apps.append({
        "id": secrets.token_hex(4),
        "name": request.form.get("name", "").strip(),
        "url": request.form.get("url", "").strip(),
        "icon": request.form.get("icon", "").strip(),
    })
    save_apps(apps)
    return redirect(url_for("manage"))


@app.post("/manage/edit/<app_id>")
@login_required
def manage_edit(app_id):
    apps = load_apps()
    for a in apps:
        if a["id"] == app_id:
            a["name"] = request.form.get("name", "").strip()
            a["url"] = request.form.get("url", "").strip()
            a["icon"] = request.form.get("icon", "").strip()
    save_apps(apps)
    return redirect(url_for("manage"))


@app.post("/manage/delete/<app_id>")
@login_required
def manage_delete(app_id):
    apps = [a for a in load_apps() if a["id"] != app_id]
    save_apps(apps)
    return redirect(url_for("manage"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
