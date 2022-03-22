from asyncio.windows_events import NULL
#from crypt import methods
from turtle import title, width
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from flask_session import Session
from jinja2 import Template
from sqlalchemy import true
from helpers import apology, login_required
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, time
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
    # return render_template("top.html")


    # -----------------------------もしも一覧表示用コード（構造テスト）-------------------
    # dreams = db.execute("SELECT * FROM dreams")
    # users =  db.execute("SELECT username, id FROM users")
    # comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    # replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)



    # return render_template("test_for_mosimo.html", dreams=dreams, comments=comments, replies=replies, users=users)

    # -------------------------------もしも一覧表示用コード（構造テスト）------------------

    #------------------------------jinnaテスト用コード--------------------------------------
    # test = "jinjaは作動してる!!"

   # names = {'yuki', 'takahashi', 'aaa', 'bbb', 11}

    #db.execute("DELETE FROM users WHERE username LIKE '%i'")
    #db.execute("INSERT INTO users(username, hash, is_business) values('yuki', 'fwaofhaogoha', True)")
    #db.execute("INSERT INTO users(username, hash, is_business) values('takahashi', 'fwggoanajfha', False)")

    #users = db.execute("SELECT * FROM users")

    # -----secrets一覧テスト用コード-----

    secrets = db.execute("SELECT * FROM secrets WHERE is_deleted = ?", False)

    return render_template("test.html", test=test, secrets=secrets)

    #------------------------------jinnaテスト用コード--------------------------------------

    #------------------------------画像テスト用コード--------------------------------------
    # test = db.execute("SELECT image FROM secrets")
    # test = test [0]['image']
    # return render_template("test1.html", test=test)
    #------------------------------画像テスト用コード--------------------------------------

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
        session["is_business"] = users[0]["is_business"]

        # Redirect user to home page
        return redirect("/dreams")

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
                "INSERT INTO users (username, hash, is_business) VALUES (?, ?, ?) ", username, hash, False
            )
            # Redirect user to home page
            return redirect("/login")

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
                "INSERT INTO users (username, hash, is_business) VALUES (?, ?, ?) ", username, hash, True
            )
            # Redirect user to home page
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_b.html")

@app.route("/dreams", methods=["GET", "POST"])
@login_required
def dreams():
    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)


    # """Costomer can register new dream"""
    # is_business = db.execute("SELECT is_business FROM users WHERE id = ?", session["user_id"])

    # if is_business == False:
    if request.method == "POST":
        content = request.form.get("content")
        db.execute(
            "INSERT INTO dreams (user_id, content, is_solved, is_deleted) VALUES (?, ?, ?, ?)",
            session["user_id"],
            content,
            False,
            False
        )
        return redirect("/dreams")

    else:
        return render_template("dreams.html", dreams=dreams, users=users, comments=comments, replies=replies)

    # else:
    #     return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies)


@app.route("/search_dreams", methods=["GET", "POST"])
@login_required
def search_dreams():  
    """Show the result of quotation of dreams"""
    symbol = request.form.get("symbol")
    symbol = '%' + symbol + '%'
    quotes = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND content LIKE ? ORDER BY created_date DESC",
        False, 
        symbol
    )

    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? ORDER BY created_date DESC", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? ORDER BY created_date DESC", False)

    return render_template("search_dreams.html", quotes=quotes, users=users, comments=comments, replies=replies)



@app.route("/search_secrets", methods=["GET", "POST"])
@login_required
def search_secrets():  
    """Show the result of quotation of secrets"""
    symbol = request.form.get("symbol")
    symbol = '%' + symbol + '%'
    quotes = db.execute(
        "SELECT * FROM secrets WHERE is_deleted = ? AND content LIKE ? OR title LIKE ?",
        False,
        symbol,
        symbol
    )

    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? ORDER BY created_date DESC", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? ORDER BY created_date DESC", False)

    return render_template("search_dreams.html", quotes=quotes, users=users, comments=comments, replies=replies)


@app.route("/secrets", methods=["GET", "POST"])
@login_required
def secrets():
    """Show list of secrets.db"""
    user_id = session["user_id"] 
    secrets = db.execute("SELECT * FROM secrets WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users = db.execute("SELECT * FROM users")

    # if is_business == True:
    if request.method == "POST":
        title = request.form.get("title")
        image = request.files['image_file'] 
        # filename = request.form.get("image_file")
        tdatetime = datetime.now()
        tstr = tdatetime.strftime('%Y-%m-%d_%Hh%Mm%Ss')
        # time = datetime.strptime(tstr, '%Y/%m/%d %H:%M:%S')
        image.filename = tstr
        user = db.execute("SELECT id FROM users WHERE id =?", user_id)
        filename = str(user[0]['id']) + '_' + image.filename
        content = request.form.get("content")
        
        db.execute("INSERT INTO secrets (user_id, title, content, image, is_deleted) VALUES (?, ?, ?, ?, ?)", 
                    user_id, title, content, filename, False)

        filepath = 'static/upload_img/' + filename
        image.save(filepath)

        return redirect("/secrets")

    else:
        filenames = db.execute("SELECT image, user_id FROM secrets WHERE is_deleted = False")
        return render_template("secrets.html", secrets=secrets, users=users, filenames = filenames)

    # else:
    #     return render_template("secrets.html", secrets=secrets)


@app.route("/mypage_c")
@login_required
def mypage_c():
    """Show my dreams & comments & replies"""
    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?))",
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    best_answers = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND is_best = ? AND user_id = ?)",
        False,
        False,
        True,
        session["user_id"]
        )

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers) 



@app.route("/dream_edit", methods=["POST"])
@login_required
def dream_edit():
    """Edit my dream"""

    dream_id = request.form["dream_id"]
    content = request.form["content"]

    db.execute("UPDATE dreams SET content = ? WHERE id = ?", content, dream_id)

    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM replies WHERE user_id = ?)",
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute(
        "SELECT * FROM comments WHERE is_deleted = ? AND user_id = ? OR dreams_id IN(SELECT id FROM dreams WHERE user_id = ?) OR id IN(SELECT comments_id FROM replies WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE is_deleted = ? AND user_id = ? OR comments_id IN(SELECT id FROM comments WHERE user_id = ?) OR comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    return render_template("mydreams.html", dreams=dreams, comments=comments, replies=replies)


@app.route("/comment_edit", methods=["POST"])
@login_required
def comment_edit():
    """Edit my comment"""

    comment_id = request.form["comment_id"]
    content = request.form["content"]

    db.execute("UPDATE comments SET content = ? WHERE id = ?", content, comment_id)

    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM replies WHERE user_id = ?)",
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute(
        "SELECT * FROM comments WHERE is_deleted = ? AND user_id = ? OR dreams_id IN(SELECT id FROM dreams WHERE user_id = ?) OR id IN(SELECT comments_id FROM replies WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE is_deleted = ? AND user_id = ? OR comments_id IN(SELECT id FROM comments WHERE user_id = ?) OR comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    return render_template("mydreams.html", dreams=dreams, comments=comments, replies=replies)




@app.route("/reply_edit", methods=["POST"])
@login_required
def reply_edit():
    """Edit my reply"""

    reply_id = request.form["reply_id"]
    content = request.form["content"]

    db.execute("UPDATE replies SET content = ? WHERE id = ?", content, reply_id)

    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM replies WHERE user_id = ?)",
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute(
        "SELECT * FROM comments WHERE is_deleted = ? AND user_id = ? OR dreams_id IN(SELECT id FROM dreams WHERE user_id = ?) OR id IN(SELECT comments_id FROM replies WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
        session["user_id"]
    )
    replies = db.execute(
        "SELECT * FROM replies WHERE is_deleted = ? AND user_id = ? OR comments_id IN(SELECT id FROM comments WHERE user_id = ?) OR comments_id IN(SELECT id FROM comments WHERE dreams_id IN(SELECT id FROM dreams WHERE user_id = ?)", 
        False,
        session["user_id"],
        session["user_id"],
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
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ?", False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)
    solved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?" , False, True)
    unsolved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?", False, False)

    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, solved=solved, unsolved=unsolved)


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
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ?", False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)
    solved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?" , False, True)
    unsolved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?", False, False)

    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, solved=solved, unsolved=unsolved)


@app.route("/best_answer", methods=["POST"])
@login_required
def best_answer():
    """Select a best answer"""

    comment_id = request.form["comment_id"]

    db.execute("UPDATE comments SET is_best = ? WHERE id = ?", 1, comment_id)

    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ?", False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)
    solved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?" , False, True)
    unsolved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?", False, False)

    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, solved=solved, unsolved=unsolved)


@app.route("/solve_dream", methods=["POST"])
@login_required
def solve_dream():
    """Solve my dream"""

    dream_id = request.form["dream_id"]

    db.execute("UPDATE dreams SET is_solve = ? WHERE id = ?", True, dream_id)

    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ?", False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)
    solved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?" , False, True)
    unsolved = db.execute("SELECT * FROM replies WHERE is_deleted = ? AND is_solved = ?", False, False)

    return render_template("dreams.html", dreams=dreams, comments=comments, replies=replies, solved=solved, unsolved=unsolved)




@app.route("/dream_delete", methods=["POST"]) #To delete posts（this is for normal_user） 
@login_required
def dream_delete():
    """dream_delete"""

    user_id = session["user_id"] # insert user_id 

    # dreams_content = request.form.get("dreams_content") #Insert content into this variable. Comparison to investigate which dream is about to delete
    # dreams_id = db.execute("SELECT id FROM dreams WHERE user_id = ? AND content = ?", user_id, dreams_content)

    dreams_id = request.form.get("dreams_id") #上記の2行をあわわしている

    db.execute("UPDATE dreams SET is_deleted = True WHERE id = ? AND user_id = ?", dreams_id, user_id) #Change id_deleted == true

    #delete comments related posts that is deleted ↑ (Change 'is_deleted' into True)
    comments_id = db.execute("SELECT id FROM comments WHERE dream_id = ?", dreams_id)
    db.execute("UPDATE comments SET is_deleted = True WHERE id = ?", comments_id)

    #delete replies related comments that is deleted ↑ (Change 'is_deleted' into True)
    db.execute("UPDATE replies SET is_deleted = True WHERER comments_id = ?", comments_id)

    return redirect("mypage_c.html")

@app.route("/secrets_delete", methods=["POST"]) #To delete posts(this is for developer)
@login_required
def secrets_delete():
    """secrets_delete"""

    user_id = session["user_id"] # insert user_id 

    # secrets_content = request.form.get("secrets_content") #Insert content into this variable. Comparison to investigate which secret is about to delete
    # secrets_id = db.execute("SELECT id FROM dreams WHERE user_id = ? AND content = ?", user_id, secrets_content)

    secrets_id = request.form.get("secrets_id")


    db.execute("UPDATE secrets SET is_deleted = True WHERE id = ? AND user_id = ?", secrets_id, user_id) #Change id_deleted == true

    return redirect("mypage_b")

@app.route("/mypage_b") #To show secrets(only developer who is login)
@login_required
def mypage_b():
    user_id = session["user_id"]
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = False", user_id)

    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    best_answers = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND is_best = ? AND user_id = ?)",
        False,
        False,
        True,
        session["user_id"]
        )

    return render_template("mypage_b.html", secrets=secrets, users=users, comments=comments, replies=replies, best_answers=best_answers) 



@app.route("/show_my_best_answer") #To show best_answer(only developer who is login)
@login_required
def show_my_best_answer():
    user_id = session["user_id"]

    user = db.execute("SELECT is_business FROM users WHERE id = ?", user_id)

    """Show best answer"""
    dreams = db.execute("SELECT * FROM dreams WHERE user_id = ? AND is_deleted = False AND is_best = 1", user_id)
    comments = db.execute("SELECT * FROM comments WHERE user_id = ? AND is_deleted = False", user_id)
    replies = db.execute("SELECT * FROM replies WHERE user_id = ? AND is_deleted = False", user_id)
    if user == False:
        return render_template("mypage_c.html", dreams=dreams, comments=comments, replies=replies)
    else:
        return render_template("mypage_b.html", dreams=dreams, comments=comments, replies=replies)


@app.route("/secrets_edit", methods=["POST"]) #To edit secrets(only developer who is login)
@login_required
def secrets_edit():

    user_id = session["user_id"]

    """Edit my secrets"""

    secrets_id = request.form["secrets_id"]
    secrets_content = request.form["secrets_content"]

    db.execute("UPDATE secrets SET content = ? WHERE id = ?, user_id = ?", secrets_content, secrets_id, user_id)

    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = False", user_id)

    return render_template("mypage_b.html", secrets=secrets)


@app.route("/solved", methods=["GET", "POST"]) #this is for timeline of solved dream
@login_required
def solved():
    dreams = db.execute("SELECT * FROM dreams WHERE is_solved = ? AND is_deleted = ? ORDER BY created_date DESC", True, False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? ORDER BY created_date DESC", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users = db.execute("SELECT * FROM users")

    return render_template("search_solved.html", dreams = dreams, comments=comments, replies=replies, users=users)


@app.route("/unsolved", methods=["GET","POST"])  #this is for timeline of unsolved dream
@login_required
def unsolved():
    dreams = db.execute("SELECT * FROM dreams WHERE is_solved = ? AND is_deleted = ? ORDER BY created_date DESC", False, False)
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? ORDER BY created_date DESC", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users = db.execute("SELECT * FROM users")

    return render_template("search_unsolved.html", dreams = dreams, comments=comments, replies=replies, users=users)
    