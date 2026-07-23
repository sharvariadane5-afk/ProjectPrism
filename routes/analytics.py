from flask import Blueprint, render_template, session, redirect
from database import get_db

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    total_projects = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    ongoing = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Ongoing'"
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Completed'"
    ).fetchone()[0]

    delayed = conn.execute(
        "SELECT COUNT(*) FROM projects WHERE status='Delayed'"
    ).fetchone()[0]

    total_reports = conn.execute(
        "SELECT COUNT(*) FROM reports"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "analytics.html",
        total_projects=total_projects,
        ongoing=ongoing,
        completed=completed,
        delayed=delayed,
        total_reports=total_reports
    )