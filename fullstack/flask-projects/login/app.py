import re
import bcrypt
import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "your secret key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin123"
app.config["MYSQL_DB"] = "LOGIN_FORM_FLASK"
app.config["MYSQL_PORT"] = 5000
mysql = MySQL(app)

# Hàm kết nối cơ sở dữ liệu
def get_db_cursor():
    return mysql.connection.cursor(MySQLdb.cursors.DictCursor)

# Hàm kiểm tra tên người dùng đã tồn tại chưa
def is_username_taken(username):
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
    return cursor.fetchone() is not None

# Hàm kiểm tra mật khẩu có đúng không
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Trang đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            cursor = get_db_cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
            account = cursor.fetchone()

            if account and check_password(account["password"], password):
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = account["username"]
                return render_template("index.html", msg="Logged in successfully!")
            else:
                msg = "Incorrect username or password!"
        else:
            msg = "Please provide both username and password!"

    return render_template("login.html", msg=msg)

# Trang đăng xuất
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Trang đăng ký
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if username and password and email:
            if is_username_taken(username):
                msg = "Account already exists!"
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                msg = "Invalid email address!"
            elif not re.match(r"[A-Za-z0-9]+", username):
                msg = "Username must contain only characters and numbers!"
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor = get_db_cursor()
                cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
                mysql.connection.commit()
                msg = "You have successfully registered!"

        else:
            msg = "Please fill out all fields!"

    return render_template("register.html", msg=msg)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
