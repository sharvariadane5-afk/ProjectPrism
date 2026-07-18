from flask import Blueprint, render_template, request, redirect, session
from database import get_db

project_bp = Blueprint("projects", __name__)

# ---------------- ADD PROJECT ---------------- #

@project_bp.route("/add_project", methods=["GET", "POST"])
def add_project():

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Officer":
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]
        department = request.form["department"]
        location = request.form["location"]
        budget = request.form["budget"]
        contractor = request.form["contractor"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form["status"]
        description = request.form["description"]

        conn = get_db()

        conn.execute("""
            INSERT INTO projects
            (
                title,
                department,
                location,
                budget,
                contractor,
                start_date,
                end_date,
                status,
                description
            )
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            title,
            department,
            location,
            budget,
            contractor,
            start_date,
            end_date,
            status,
            description
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_project.html")

# ---------------- VIEW PROJECTS ---------------- #

@project_bp.route("/projects")
def view_projects():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    projects = conn.execute("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects,
        title="All Projects"
    )


# ---------------- FILTER PROJECTS ---------------- #

@project_bp.route("/projects/status/<status>")
def filter_projects(status):

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    projects = conn.execute("""
        SELECT *
        FROM projects
        WHERE status=?
        ORDER BY id DESC
    """, (status,)).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects,
        title=f"{status} Projects"
    )

# ---------------- PROJECT DETAILS ---------------- #

@project_bp.route("/project/<int:project_id>")
def project_details(project_id):

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (project_id,)
    ).fetchone()

    if project is None:
        conn.close()
        return "Project Not Found"

    updates = conn.execute("""

        SELECT *
        FROM progress_updates

        WHERE project_id=?

        ORDER BY id DESC

    """,

    (project_id,)).fetchall()

    conn.close()

    return render_template(
        "project_details.html",
        project=project,
        updates=updates
    )

# ---------------- ADD PROGRESS ---------------- #

@project_bp.route("/project/<int:project_id>/progress", methods=["GET", "POST"])
def add_progress(project_id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Officer":
        return "Access Denied"

    conn = get_db()

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (project_id,)
    ).fetchone()

    if project is None:
        conn.close()
        return "Project Not Found"

    if request.method == "POST":

        progress = request.form["progress"]
        remarks = request.form["remarks"]
        update_date = request.form["update_date"]

        conn.execute("""

        INSERT INTO progress_updates
        (
            project_id,
            progress,
            remarks,
            update_date
        )

        VALUES(?,?,?,?)

        """,

        (
            project_id,
            progress,
            remarks,
            update_date
        ))

        conn.commit()
        conn.close()

        return redirect(f"/project/{project_id}")

    conn.close()

    return render_template(
        "add_progress.html",
        project=project
    )