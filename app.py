import os
from flask import Flask
from database import create_tables

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.secret_key = "projectprism"

create_tables()

# Register Blueprints
from routes.reports import reports_bp
from routes.auth import auth_bp
from routes.projects import project_bp
from routes.analytics import analytics_bp
from routes.documents import documents_bp

app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(project_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(documents_bp)

if __name__ == "__main__":
    app.run(debug=True)