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
        (title,
        department,
        location,
        budget,
        contractor,
        start_date,
        end_date,
        status,
        approval_status,
        description)

        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,

        (
        title,
        department,
        location,
        budget,
        contractor,
        start_date,
        end_date,
        status,
        "Pending",
        description
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_project.html")

# ---------------- SEARCH PROJECTS ---------------- #

@project_bp.route("/search_projects")
def search_projects():

    if "user_id" not in session:
        return redirect("/")

    keyword = request.args.get("keyword", "")
    status = request.args.get("status", "")

    conn = get_db()

    if keyword and status:

        projects = conn.execute("""

        SELECT *
        FROM projects
        WHERE title LIKE ?
        AND status=?

        ORDER BY id DESC

        """,

        ('%' + keyword + '%', status)

        ).fetchall()

    elif keyword:

        projects = conn.execute("""

        SELECT *
        FROM projects
        WHERE title LIKE ?

        ORDER BY id DESC

        """,

        ('%' + keyword + '%',)

        ).fetchall()

    elif status:

        projects = conn.execute("""

        SELECT *
        FROM projects
        WHERE status=?

        ORDER BY id DESC

        """,

        (status,)

        ).fetchall()

    else:

        projects = conn.execute("""

        SELECT *
        FROM projects
        ORDER BY id DESC

        """).fetchall()

    conn.close()

    return render_template(

        "projects.html",

        projects=projects,

        title="Search Results"

    )

# ---------------- VIEW PROJECTS ---------------- #

@project_bp.route("/projects")
def view_projects():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    projects = conn.execute("""
        SELECT * FROM projects
        WHERE approval_status='Approved'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects,
        title="All Projects"
    )


# ---------------- APPROVE PROJECT ---------------- #
@project_bp.route("/project/<int:project_id>/approve")
def approve_project(project_id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    conn.execute("""
    UPDATE projects
    SET approval_status='Approved'
    WHERE id=?
    """, (project_id,))

    conn.commit()
    conn.close()

    return redirect("/pending-projects")


# ---------------- REJECT PROJECT ---------------- #
@project_bp.route("/project/<int:project_id>/reject")
def reject_project(project_id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    conn.execute("""
    UPDATE projects
    SET approval_status='Rejected'
    WHERE id=?
    """, (project_id,))

    conn.commit()
    conn.close()

    return redirect("/pending-projects")

# ---------------- PENDING PROJECTS ---------------- #

@project_bp.route("/pending-projects")
def pending_projects():

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "Admin":
        return "Access Denied"

    conn = get_db()

    projects = conn.execute("""
    SELECT *
    FROM projects
    WHERE approval_status='Pending'
    """).fetchall()

    conn.close()

    return render_template(
        "pending_projects.html",
        projects=projects
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

# ---------------- EDIT PROJECT ---------------- #

@project_bp.route("/project/<int:project_id>/edit", methods=["GET","POST"])
def edit_project(project_id):

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        status = request.form["status"]

        conn.execute(
            """
            UPDATE projects
            SET title=?,
                description=?,
                status=?
            WHERE id=?
            """,
            (title, description, status, project_id)
        )

        conn.commit()
        conn.close()

        return redirect(f"/project/{project_id}")

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (project_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_project.html",
        project=project
    )

# ---------------- DELETE PROJECT ---------------- #
@project_bp.route("/project/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    conn.execute(
        "DELETE FROM projects WHERE id=?",
        (project_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/projects")

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