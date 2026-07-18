from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
from database import get_db

from flask import render_template,request,redirect,session


print("auth.py loaded")
# ---------------- LOGIN ---------------- #

@auth_bp.route("/", methods=["GET","POST"])
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

@auth_bp.route("/signup",methods=["GET","POST"])
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

@auth_bp.route("/dashboard")
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

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")