from flask import Blueprint
from database import get_db
from flask import render_template, request, redirect, session

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/report/<int:project_id>", methods=["GET","POST"])
def report_issue(project_id):

    if "user_id" not in session:
        return redirect("/")

    if request.method=="POST":

        issue=request.form["issue"]
        description=request.form["description"]

        conn=get_db()

        conn.execute("""

        INSERT INTO reports(
            project_id,
            user_id,
            issue,
            description
        )

        VALUES(?,?,?,?)

        """,

        (
            project_id,
            session["user_id"],
            issue,
            description
        ))

        conn.commit()
        conn.close()

        return redirect("/project/" + str(project_id))

    return render_template(
        "report_issue.html",
        project_id=project_id
    )

@reports_bp.route("/reports")
def view_reports():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    reports = conn.execute("""

    SELECT
        reports.id,
        reports.issue,
        reports.description,
        reports.status,
        reports.created_at,
        projects.title

    FROM reports

    JOIN projects
    ON reports.project_id = projects.id

    ORDER BY reports.id DESC

    """).fetchall()

    conn.close()

    return render_template(
        "reports.html",
        reports=reports
    )

@reports_bp.route("/report/<int:report_id>/resolve")
def resolve_report(report_id):

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    conn.execute("""

    UPDATE reports

    SET status='Resolved'

    WHERE id=?

    """,(report_id,))

    conn.commit()

    conn.close()

    return redirect("/reports")