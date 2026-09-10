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
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

DATA_FILE = os.environ.get("LOBBY_DATA_FILE", os.path.join(app.root_path, "data", "apps.json"))
DATA_DIR = os.path.dirname(DATA_FILE)
SEED_FILE = os.path.join(app.root_path, "apps.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SECRET_KEY_FILE = os.path.join(DATA_DIR, "secret_key")


def get_secret_key():
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SECRET_KEY_FILE):
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(secrets.token_hex(32))
    with open(SECRET_KEY_FILE) as f:
        return f.read().strip()


app.secret_key = get_secret_key()
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=365)

login_manager = LoginManager(app)
login_manager.login_view = "login"


def load_apps():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        shutil.copy(SEED_FILE, DATA_FILE)
    with open(DATA_FILE) as f:
        return json.load(f)


def save_apps(apps):
    with open(DATA_FILE, "w") as f:
        json.dump(apps, f, indent=2)


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)


def save_users(users):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    return User(user_id) if user_id in users else None


@app.get("/setup")
def setup():
    if load_users():
        return redirect(url_for("login"))
    return render_template("setup.html")


@app.post("/setup")
def setup_post():
    if load_users():
        return redirect(url_for("login"))
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        return render_template("setup.html", error="Username and password required"), 400
    save_users({username: generate_password_hash(password)})
    login_user(User(username), remember=True)
    return redirect(url_for("index"))


@app.get("/login")
def login():
    if not load_users():
        return redirect(url_for("setup"))
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.post("/login")
def login_post():
    users = load_users()
    if not users:
        return redirect(url_for("setup"))
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username in users and check_password_hash(users[username], password):
        login_user(User(username), remember=True)
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
    return render_template("manage.html", apps=load_apps(), users=load_users(), current_user=current_user)


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


@app.post("/manage/users/add")
@login_required
def manage_users_add():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if username and password:
        users = load_users()
        users[username] = generate_password_hash(password)
        save_users(users)
    return redirect(url_for("manage"))


@app.post("/manage/users/delete/<username>")
@login_required
def manage_users_delete(username):
    users = load_users()
    if len(users) > 1 and username in users:
        users.pop(username)
        save_users(users)
        if username == current_user.id:
            logout_user()
            return redirect(url_for("login"))
    return redirect(url_for("manage"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
