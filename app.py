from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "projectprism"


# ---------------- DATABASE ---------------- #

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        department TEXT NOT NULL,
        location TEXT NOT NULL,
        budget REAL NOT NULL,
        contractor TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        status TEXT,
        description TEXT

    )
    """)

    conn.commit()
    conn.close()


create_tables()


# ---------------- LOGIN ---------------- #

@app.route("/", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=get_db()

        user=conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"]=user["id"]
            session["name"]=user["name"]
            session["role"]=user["role"]

            return redirect("/dashboard")

        else:
            return "Invalid Login"

    return render_template("login.html")


# ---------------- SIGNUP ---------------- #

@app.route("/signup",methods=["GET","POST"])
def signup():

    if request.method=="POST":

        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        role=request.form["role"]

        conn=get_db()

        conn.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (name,email,password,role)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("signup.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    total_projects = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Completed'"
    ).fetchone()[0]

    ongoing = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Ongoing'"
    ).fetchone()[0]

    delayed = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Delayed'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",

        total_projects=total_projects,

        completed=completed,

        ongoing=ongoing,

        delayed=delayed
    )

# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)