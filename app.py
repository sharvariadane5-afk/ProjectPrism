from flask import Flask
from database import create_tables

app = Flask(__name__)
app.secret_key = "projectprism"

create_tables()

# Register Blueprints
from routes.auth import auth_bp
from routes.projects import project_bp

app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)