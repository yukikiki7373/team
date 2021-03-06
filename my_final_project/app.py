from asyncio.windows_events import NULL
from traceback import print_tb
#from crypt import methods
from turtle import title, width
from cs50 import SQL
from flask import Flask, before_render_template, flash, redirect, render_template, request, session
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

   

@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", apology = "ユーザー名を入力してください", code = 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", apology="パスワードを入力してください", code = 403)

        # Query database for username
        users = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(
            users[0]["hash"], request.form.get("password")
        ):
            return render_template("apology.html", apology = "ユーザー名またはパスワードが間違っています", code = 403)

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
            return ("ユーザー名を入力してください", 400)
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            return render_template("apology.html", apology = "このユーザー名は既に登録されています", code = 400)

        # Ensure password was submitted
        elif not password:
            return render_template("apology.html", apology = "パスワードを入力してください", code = 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return render_template("apology.html", apology = "パスワード（確認）を入力してください", code = 400)

        # Ensure passwords match
        elif not password == confirmation:
            return render_template("apology.html", apology = "同じパスワードを入力してください", code = 400)

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
            return render_template("apology.html", apology = "ユーザー名を入力してください", code = 400)
        # Ensure the username doesn't exists
        elif len(rows) != 0:
            return render_template("apology.html", apology = "このユーザー名は既に登録されています", code = 400)

        # Ensure password was submitted
        elif not password:
            return render_template("apology.html", apology = "パスワードを入力してください", code = 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return render_template("apology.html", apology = "パスワード（確認）を入力してください", code = 400)

        # Ensure passwords match
        elif not password == confirmation:
            return render_template("apology.html", apology = "同じパスワードを入力してください", code = 400)

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

    if request.method == "POST":
        content = request.form.get("content")
        db.execute(
            "INSERT INTO dreams (user_id, content, is_solved, is_deleted) VALUES (?, ?, ?, ?)",
            session["user_id"],
            content,
            False,
            False
        )
        flash("投稿が完了しました")
        return redirect("/dreams")

    else:
        return render_template("dreams.html", dreams=dreams, users=users, comments=comments, replies=replies)


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
        "SELECT * FROM secrets WHERE is_deleted = ? AND content LIKE ? OR title LIKE ? ORDER BY created_date DESC",
        False,
        symbol,
        symbol
    )

    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ? ORDER BY created_date DESC", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ? ORDER BY created_date DESC", False)
    filenames = db.execute("SELECT image, user_id FROM secrets WHERE is_deleted = False")

    return render_template("search_secrets.html", quotes=quotes, users=users, comments=comments, replies=replies, filenames=filenames)


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

        flash("投稿が完了しました。")
        return redirect("/secrets")

    else:
        filenames = db.execute("SELECT image, user_id FROM secrets WHERE is_deleted = False")
        return render_template("secrets.html", secrets=secrets, users=users, filenames = filenames)


@app.route("/mypage_c")
@login_required
def mypage_c():
    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies) 



@app.route("/dream_edit", methods=["POST"])
@login_required
def dream_edit():
    """Edit my dream"""

    id = request.form["id"]
    content = request.form["content"]

    db.execute("UPDATE dreams SET content = ? WHERE id = ?", content, id)
    flash("編集が完了しました。")

    """Show my dreams & comments & replies"""
    dreams = db.execute(
            "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
            False,
            session["user_id"],
            session["user_id"],
            False,
            False,
            session["user_id"],
            False
        )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies) 

@app.route("/comment", methods=["POST"])
@login_required
def comment():
    """Add comment to a dream"""

    dreams_id = request.form["dreams_id"]
    content = request.form["content"]

    db.execute(
        "INSERT INTO comments (user_id, dreams_id, content, is_best, is_deleted) VALUES (?, ?, ?, ?, ?)",
        session["user_id"],
        dreams_id,
        content,
        False,
        False
    )
    flash("コメントを投稿しました。")

    """Show list of dreams.db"""
    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("dreams.html", dreams=dreams, users=users, comments=comments, replies=replies)


@app.route("/reply", methods=["POST"])
@login_required
def reply():
    """Add reply to a comment"""

    comments_id = request.form["comments_id"]
    content = request.form["content"]

    db.execute(
        "INSERT INTO replies (user_id, comments_id, content, is_deleted) VALUES (?, ?, ?, ?)",
        session["user_id"],
        comments_id,
        content,
        False
    )
    flash("リプライを投稿しました。")

    """Show list of dreams.db"""
    """Show list of dreams.db"""
    dreams = db.execute("SELECT * FROM dreams WHERE is_deleted = ? ORDER BY created_date DESC", False)
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("dreams.html", dreams=dreams, users=users, comments=comments, replies=replies)


@app.route("/best_answer", methods=["POST"])
@login_required
def best_answer():
    """Select a best answer"""
    comment_id = request.form.get("comment_id")

    db.execute("UPDATE comments SET is_best = ? WHERE id = ?", True, comment_id)
    db.execute("UPDATE dreams SET is_solved = ? WHERE id IN(SELECT dreams_id FROM comments WHERE id = ?)", True, comment_id)
    flash("ベストアンサーを登録しました。")
    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies) 


@app.route("/cancel_best_answer", methods=["POST"])
@login_required
def cancel_best_answer():
    """Cancel a best answer"""
    comment_id = request.form.get("comment_id")
    db.execute("UPDATE comments SET is_best = ? WHERE id = ?", False, comment_id)
    db.execute("UPDATE dreams SET is_solved = ? WHERE id IN(SELECT dreams_id FROM comments WHERE id = ?)", False, comment_id)
    flash("ベストアンサーを取り消しました。")

    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies) 



@app.route("/dream_delete", methods=["POST"]) #To delete posts（this is for normal_user） 
@login_required
def dream_delete():
    """dream_delete"""

    user_id = session["user_id"]
    id = request.form["id"]

    db.execute("UPDATE dreams SET is_deleted = ? WHERE id = ? AND user_id = ?", True, id, user_id) #Change id_deleted == true
    flash("投稿を削除しました。")

    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies) 



@app.route("/comment_delete", methods=['POST']) #To delete posts（this is for normal_user） 
@login_required
def comment_delete():
    """dream_delete"""
    comment_id = request.form.get("comment_id")
    print(comment_id)
    db.execute("UPDATE comments SET is_deleted = ? WHERE id = ? AND user_id = ?", True, comment_id, session["user_id"]) #Change id_deleted == true
    flash("コメントを削除しました。")
    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies)  

@app.route("/reply_delete", methods=['POST']) #To delete posts（this is for normal_user） 
@login_required
def reply_delete():
    """reply_delete"""
    reply_id = request.form.get("reply_id")
    db.execute("UPDATE replies SET is_deleted = ? WHERE id = ? AND user_id = ?", True, reply_id, session["user_id"]) #Change id_deleted == true
    flash("リプライを削除しました。")
    """Show my dreams & comments & replies"""
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND user_id = ? OR id IN(SELECT dreams_id FROM comments WHERE user_id = ? AND is_deleted = ?) OR id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND id IN(SELECT comments_id FROM replies WHERE user_id = ? AND is_deleted = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"],
        False,
        False,
        session["user_id"],
        False
    )
    users =  db.execute("SELECT username, id FROM users")
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    return render_template("mypage_c.html", users=users, dreams=dreams, comments=comments, replies=replies)  



@app.route("/secrets_delete", methods=["POST"]) #To delete posts(this is for developer)
@login_required
def secrets_delete():
    """secrets_delete"""
    user_id = session["user_id"]
    id = request.form.get("secret_id")

    db.execute("UPDATE secrets SET is_deleted = ? WHERE id = ? AND user_id = ?", True, id, user_id) #Change id_deleted == true
    flash("ひみつ道具投稿を削除しました。")
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = False", user_id)

    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?)) ORDER BY created_date DESC",
        False,
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

    return redirect("/mypage_b")
    # return render_template("mypage_b.html", secrets=secrets, users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers) 


@app.route("/mypage_b") #To show secrets(only developer who is login)
@login_required
def mypage_b():
    user_id = session["user_id"]
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = ? ORDER BY created_date DESC", user_id, False)
    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    best_answers = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND is_best = ? AND user_id = ? ORDER BY created_date DESC)",
        False,
        False,
        True,
        session["user_id"]
        )
    
    filenames = db.execute("SELECT image, user_id FROM secrets WHERE is_deleted = False")

    return render_template("mypage_b.html", secrets=secrets, users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers, filenames=filenames) 

@app.route("/image_edit", methods=["POST"]) #To edit image (only developer who is login)
@login_required
def image_edit():
    user_id = session["user_id"]
    secrets_id = request.form.get("secret_id")
    
    image = request.files['image_file'] 
    # filename = request.form.get("image_file")
    tdatetime = datetime.now()
    tstr = tdatetime.strftime('%Y-%m-%d_%Hh%Mm%Ss')
    # time = datetime.strptime(tstr, '%Y/%m/%d %H:%M:%S')
    image.filename = tstr
    user = db.execute("SELECT id FROM users WHERE id =?", user_id)
    filename = str(user[0]['id']) + '_' + image.filename
        
    db.execute("UPDATE secrets SET image = ? WHERE id = ?", filename, secrets_id)

    # before_filename = db.execute("SELECT image FROM secrets WHERE id = ?", secrets_id)
    # before_filename = before_filename[0]['image']
    # # if os.path.exists('before_filename'):
    # before_filename = 'static/upload_img/' + before_filename
    # os.remove(before_filename)
    
    filepath = 'static/upload_img/' + filename
    image.save(filepath)

    filenames = db.execute("SELECT image, user_id FROM secrets WHERE is_deleted = False")


    user_id = session["user_id"]
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = False", user_id)

    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?))",
        False,
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

    return render_template("mypage_b.html", secrets=secrets, users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers, filenames=filenames) 


@app.route("/title_edit", methods=["POST"]) #To edit secrets(only developer who is login)
@login_required
def title_edit():

    """Edit my title of secrets"""

    id = request.form.get("title_id")
    title = request.form.get("title_update_txt")

    db.execute("UPDATE secrets SET title = ? WHERE id = ?", title, id)
    flash("編集が完了しました。")

    user_id = session["user_id"]
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = ? ORDER BY created_date DESC", user_id, False)

    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?)) ORDER BY created_date DESC",
        False,
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
    return redirect("/mypage_b")
    # return render_template("mypage_b.html", secrets=secrets, users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers) 


@app.route("/content_edit", methods=["POST"]) #To edit secrets(only developer who is login)
@login_required
def content_edit():
    """Edit my content of secrets"""

    id = request.form.get("content_id")
    content = request.form.get("content_update_txt")

    db.execute("UPDATE secrets SET content = ? WHERE id = ?", content, id)
    flash("編集が完了しました。")

    user_id = session["user_id"]
    """Show my secrets"""
    secrets = db.execute("SELECT * FROM secrets WHERE user_id = ? AND is_deleted = ? ORDER BY created_date DESC", user_id, False)

    users =  db.execute("SELECT username, id FROM users")
    dreams = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE user_id = ?) OR id IN(SELECT dreams_id FROM comments WHERE id IN(SELECT comments_id FROM replies WHERE user_id = ?)) ORDER BY created_date DESC",
        False,
        session["user_id"],
        session["user_id"]
    )
    comments = db.execute("SELECT * FROM comments WHERE is_deleted = ?", False)
    replies = db.execute("SELECT * FROM replies WHERE is_deleted = ?", False)

    best_answers = db.execute(
        "SELECT * FROM dreams WHERE is_deleted = ? AND id IN(SELECT dreams_id FROM comments WHERE is_deleted = ? AND is_best = ? AND user_id = ?) ORDER BY created_date DESC",
        False,
        False,
        True,
        session["user_id"]
        )
    return redirect("/mypage_b")
    # return render_template("mypage_b.html", secrets=secrets, users=users, dreams=dreams, comments=comments, replies=replies, best_answers=best_answers) 


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
    

@app.route("/ranking", methods=["GET","POST"])  #this is for timeline of unsolved dream
@login_required
def ranking():

    tests = db.execute("SELECT user_id, username, SUM(is_best) FROM users INNER JOIN comments ON users.id = comments.user_id WHERE comments.is_deleted = ? GROUP BY username ORDER BY SUM(is_best) DESC", False)

    db.execute("UPDATE comments SET is_best = False WHERE is_deleted = True")

    return render_template("ranking.html", tests=tests)