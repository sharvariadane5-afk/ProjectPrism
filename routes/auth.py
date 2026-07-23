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

    pending = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE approval_status='Pending'"
    ).fetchone()[0]

    recent_projects = conn.execute("""
    SELECT title, status
    FROM projects
    ORDER BY id DESC
    LIMIT 5
    """).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",

        total_projects=total_projects,

        completed=completed,

        ongoing=ongoing,

        delayed=delayed,

        pending=pending,

        recent_projects=recent_projects
    )

# ---------------- USERS ---------------- #
@auth_bp.route("/users")
def users():

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    users = conn.execute(
        "SELECT * FROM users ORDER BY id"
    ).fetchall()

    conn.close()

    return render_template(
        "users.html",
        users=users
    )

# ---------------- EDIT USER ---------------- #
@auth_bp.route("/user/<int:user_id>/edit", methods=["GET","POST"])
def edit_user(user_id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    if request.method == "POST":

        role = request.form["role"]

        conn.execute(
            "UPDATE users SET role=? WHERE id=?",
            (role, user_id)
        )

        conn.commit()
        conn.close()

        return redirect("/users")

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_user.html",
        user=user
    )

# ---------------- DELETE USER---------------- #
@auth_bp.route("/user/<int:user_id>/delete")
def delete_user(user_id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    conn.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/users")

# ---------------- LOGOUT ---------------- #

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")

