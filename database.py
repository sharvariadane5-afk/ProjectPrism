import sqlite3

DATABASE = "database.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_db()

    # USERS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL

    )
    """)

    # PROJECTS
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

    # PROGRESS UPDATES
    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress_updates(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            project_id INTEGER NOT NULL,

            progress INTEGER NOT NULL,

            remarks TEXT,

            update_date TEXT NOT NULL,

            FOREIGN KEY(project_id) REFERENCES projects(id)

    )
    """)

    conn.commit()

    conn.close()