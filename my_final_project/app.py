from asyncio.windows_events import NULL
from turtle import title
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
def top():
    return render_template("top.html")

@app.route("/dreams", methods=["GET", "POST"])
@login_required
def dreams():
    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ?", 0)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? AND dreams_id IN(SELECT id FROM dreams WHERE is_deleted = ?)", 0, 0)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND comments_id IN(SELECT id FROM comments WHERE is_deleted = ?)", 0, 0)

    """Show the result of quotation"""
    keyword = request.form.get("keyword")
    quote = db.execute("SELECT * FROM dreams WHERE is_deleted = ? AND content LIKE ?", 0, keyword)

    """Costomer can register new dream"""
    is_business = db.execute("SELECT is_business FROM users WHERE id = ?", session["user_id"])

    if is_business == 0:
        if request.method == "POST":
            content = request.form.get("content")
            db.execute(
                "INSERT INTO dreams (user_id, content) VALUES (?, ?)",
                session["user_id"],
                content
            )
            return redirect("/")

        else:
            return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, quote=quote)

    else:
        return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, quote=quote)


@app.route("/secrets", methods=["GET", "POST"])
@login_required
def secrets():
    """Show list of secrets.db"""
    secrets = db.execute("SELECT * FROM secrets WHERE is_deleted = ?", 0)

    """Show the result of quotation"""
    keyword = request.form.get("keyword")
    quote = db.execute("SELECT * FROM secrets WHERE is_deleted = ? AND content LIKE ?", 0, keyword)

    """Business users can register new dream"""
    is_business = db.execute("SELECT is_business FROM users WHERE id = ?", session["user_id"])

    if is_business == 1:
        if request.method == "POST":
            title = request.form.get("title")
            content = request.form.get("content")
            image = request.form.get("image")
            db.execute(
                "INSERT INTO secrets (user_id, title, content, image) VALUES (?, ?, ?, ?)",
                session["user_id"],
                title,
                content,
                image
            )
            return redirect("/")

        else:
            return render_template("secrets.html", secrets=secrets, quote=quote)

    else:
        return render_template("secrets.html", secrets=secrets, quote=quote)


@app.route("/mydreams")
@login_required
def mydreams():
    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM replies WHERE user_id = ?)",
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute(
        "SELECT * FROM comments WHERE user_id = ? OR dreams_id IN(SELECT id FROM dreams WHERE user_id = ?) OR id IN(SELECT comments_id FROM replies WHERE user_id = ?)", 
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        session["user_id"]
    )
    return render_template("mydreams.html", dreams=dreams, comments=comments, replies=replies)


@app.route("/dream_edit", methods=["POST"])
@login_required
def dream_edit():
    """Edit my dream"""

    dream_id = request.form["dream_id"]
    content = request.form["content"]

    db.execute("UPDATE dreams SET content = ? WHERE id = ?", content, dream_id)

    """Show my dreams"""
    dreams = db.execute("SELECT * FROM dreams WHERE user_id = ?", session["user_id"])
    comments = db.execute(
        "SELECT * FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        session["user_id"]
    )
    return render_template("mydreams.html", dreams=dreams, comments=comments, replies=replies)


@app.route("/comment_edit", methods=["POST"])
@login_required
def dream_edit():
    """Edit my dream"""

    dream_id = request.form["dream_id"]
    content = request.form["content"]

    db.execute("UPDATE dreams SET content = ? WHERE id = ?", content, dream_id)

    """Show my dreams"""
    dreams = db.execute("SELECT * FROM dreams WHERE user_id = ?", session["user_id"])
    comments = db.execute(
        "SELECT * FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        session["user_id"]
    )
    return render_template("mydreams.html", dreams=dreams, comments=comments, replies=replies)

@app.route("/comment", methods=["POST"])
@login_required
def comment():
    """Add comment to a dream"""

    dreams_id = request.form["dreams_id"]
    content = request.form["content"]

    db.execute(
        "INSERT INTO comments (user_id, dreams_id, content) VALUES (?, ?, ?)",
        session["user_id"],
        dreams_id,
        content,
    )

    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams")
    comments = db.execute("SELECT * FROM comments")
    replies = db.execute("SELECT * FROM replies")

    """Show the result of quotation"""
    keyword = request.form.get("keyword")
    quote = db.execute("SELECT * FROM dreams LIKE "%keyword%"")
    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, quote=quote)


@app.route("/reply", methods=["POST"])
@login_required
def reply():
    """Add reply to a comment"""

    comments_id = request.form["comments_id"]
    content = request.form["content"]

    db.execute(
        "INSERT INTO replies (user_id, comments_id, content) VALUES (?, ?, ?)",
        session["user_id"],
        comments_id,
        content,
    )

    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams")
    comments = db.execute("SELECT * FROM comments")
    replies = db.execute("SELECT * FROM replies")

    """Show the result of quotation"""
    keyword = request.form.get("keyword")
    quote = db.execute("SELECT * FROM dreams LIKE "%keyword%"")
    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, quote=quote)


@app.route("/best_answer", methods=["POST"])
@login_required
def best_answer():
    """Select a best answer"""

    comment_id = request.form["comment_id"]

    db.execute("UPDATE comments SET is_best = ? WHERE id = ?", 1, comment_id)

    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams")
    comments = db.execute("SELECT * FROM comments")
    replies = db.execute("SELECT * FROM replies")

    """Show the result of quotation"""
    keyword = request.form.get("keyword")
    quote = db.execute("SELECT * FROM dreams LIKE "%keyword%"")
    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, quote=quote)



# @app.route("/learned_edit", methods=["POST"])
# @login_required
# def learned_edit():
#     """Edit my learned"""

#     id = request.form["id"]
#     learned = request.form["learned"]

#     db.execute("UPDATE posts SET learned = ? WHERE id = ?", learned, id)

#     flash("編集が完了しました。")

#     posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
#     return render_template("mypost.html", posts=posts)


# @app.route("/help_edit", methods=["POST"])
# @login_required
# def help_edit():

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
            return redirect("/dreams")

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
            return redirect("/dreams")

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


@app.route("/dream_delete", methods=["POST"]) #To delete posts（this is for normal_user） 
@login_required
def dream_delete():
    """dream_delete"""

    user_id = session["user_id"] # insert user_id 
    dreams_content = request.form.get("dreams_content") #Insert content into this variable. Comparison to investigate which dream is about to delete
    dreams_id = db.execute("SELECT id FROM dreams WHERE user_id = ? AND content = ?", user_id, dreams_content)

    db.execute("UPDATE dreams SET is_deleted = 1 WHERE id = ? AND user_id = ?", dreams_id, user_id) #Change id_deleted == true

    #delete comments related posts that is deleted ↑ (Change 'is_deleted' into 1)
    comments_id = db.execute("SELECT id FROM comments WHERE dream_id = ?", dreams_id)
    db.execute("UPDATE comments SET is_deleted = 1 WHERE id = ?", comments_id)

    #delete replies related comments that is deleted ↑ (Change 'is_deleted' into 1)
    db.execute("UPDATE replies SET is_deleted = 1 WHERER comments_id = ?", comments_id)

    return render_template("/")#これの遷移先が不明のため後で質問する

@app.route("/secrets_delete", methods=["POST"]) #To delete posts(this is for developer)
@login_required
def secrets_delete():
    """secrets_delete"""

    user_id = session["user_id"] # insert user_id 
    secrets_content = request.form.get("secrets_content") #Insert content into this variable. Comparison to investigate which secret is about to delete
    secrets_id = db.execute("SELECT id FROM dreams WHERE user_id = ? AND content = ?", user_id, secrets_content)

    db.execute("UPDATE secrets SET is_deleted = 1 WHERE id = ? AND user_id = ?", secrets_id, user_id) #Change id_deleted == true

    return render_template("/")#これの遷移先が不明のため後で質問する