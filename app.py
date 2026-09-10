import json
import os
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
    with open(os.path.join(app.root_path, "apps.json")) as f:
        apps = json.load(f)
    return render_template("index.html", apps=apps)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
