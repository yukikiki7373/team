from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from flask_session import Session
from sqlalchemy import true
from helpers import apology, login_required
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///teamSQLite/team.db")


@app.route("/")
@login_required
def dreams():
    return render_template("dreams.html")

@app.route("/list")
@login_required
def list():
    """Show list of sotsuron.db"""
    posts = db.execute("SELECT * FROM posts")
    return render_template("list.html", posts=posts)

@app.route("/post_register", methods=["GET", "POST"])
@login_required
def post_register():
    """Register new post"""

    if request.method == "POST":
        title = request.form.get("title")
        overview = request.form.get("overview")
        content = request.form.get("content")
        learned = request.form.get("learned")
        help = request.form.get("help")

        db.execute(
            "INSERT INTO posts (user_id, title, overview, content, learned, help) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            title,
            overview,
            content,
            learned,
            help
        )

        flash("投稿が完了しました。")
        return redirect("/")

    else:
        return render_template("post_register.html")

@app.route("/mypost")
@login_required
def mypost():
    """Show my post"""
    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/title_edit", methods=["POST"])
@login_required
def title_edit():
    """Edit my title"""

    id = request.form["id"]
    title = request.form["title"]

    db.execute("UPDATE posts SET title= ? WHERE id = ?", title, id)

    flash("編集が完了しました。")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/overview_edit", methods=["POST"])
@login_required
def overview_edit():
    """Edit my overview"""

    id = request.form["id"]
    overview = request.form["overview"]

    db.execute("UPDATE posts SET overview = ? WHERE id = ?", overview, id)

    flash("編集が完了しました。")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/content_edit", methods=["POST"])
@login_required
def content_edit():
    """Edit my content"""

    id = request.form["id"]
    content = request.form["content"]

    db.execute("UPDATE posts SET content = ? WHERE id = ?", content, id)

    flash("編集が完了しました。")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/learned_edit", methods=["POST"])
@login_required
def learned_edit():
    """Edit my learned"""

    id = request.form["id"]
    learned = request.form["learned"]

    db.execute("UPDATE posts SET learned = ? WHERE id = ?", learned, id)

    flash("編集が完了しました。")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/help_edit", methods=["POST"])
@login_required
def help_edit():
    """Edit my help"""

    id = request.form["id"]
    help = request.form["help"]

    db.execute("UPDATE posts SET help = ? WHERE id = ?", help, id)

    flash("編集が完了しました。")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("mypost.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("ユーザー名を入力してください", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("パスワードを入力してください", 403)

        # Query database for username
        users = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(
            users[0]["hash"], request.form.get("password")
        ):
            return apology("ユーザー名またはパスワードが間違っています", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register_b", methods=["GET", "POST"])
def register_b():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure the username was submitted
        if not username:
            return apology("ユーザー名を入力してください", 400)
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            return apology("このユーザー名は既に登録されています", 400)

        # Ensure password was submitted
        elif not password:
            return apology("パスワードを入力してください", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("パスワード（確認）を入力してください", 400)

        # Ensure passwords match
        elif not password == confirmation:
            return apology("同じパスワードを入力してください", 400)

        else:
            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            db.execute(
                "INSERT INTO users (username, hash, is_business) VALUES (?, ?, ?) ", username, hash, true
            )
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_b.html")

@app.route("/register_c", methods=["GET", "POST"])
def register_c():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure the username was submitted
        if not username:
            return apology("ユーザー名を入力してください", 400)
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            return apology("このユーザー名は既に登録されています", 400)

        # Ensure password was submitted
        elif not password:
            return apology("パスワードを入力してください", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("パスワード（確認）を入力してください", 400)

        # Ensure passwords match
        elif not password == confirmation:
            return apology("同じパスワードを入力してください", 400)

        else:
            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?) ", username, hash
            )
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_c.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
