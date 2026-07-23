from flask import Blueprint, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from database import get_db
import os

documents_bp = Blueprint("documents", __name__)

@documents_bp.route("/project/<int:project_id>/upload", methods=["GET","POST"])
def upload_document(project_id):

    if "user_id" not in session:
        return redirect("/")

    if request.method=="POST":

        file=request.files["document"]

        if file.filename!="":

            filename=secure_filename(file.filename)

            filepath=os.path.join("uploads", filename)

            file.save(filepath)

            conn=get_db()

            conn.execute("""

            INSERT INTO documents(project_id,filename)

            VALUES(?,?)

            """,(project_id,filename))

            conn.commit()

            conn.close()

        return redirect(f"/project/{project_id}")

    return render_template(
        "upload_document.html",
        project_id=project_id
    )