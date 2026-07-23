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

        approval_status TEXT DEFAULT 'Pending',

        description TEXT

    )
    """)

    conn.execute("""
     CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        filename TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(project_id) REFERENCES projects(id)

    );
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


    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            project_id INTEGER,

            user_id INTEGER,

            issue TEXT,

            description TEXT,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(project_id) REFERENCES projects(id),

            FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    try:
        conn.execute("""
            ALTER TABLE projects
            ADD COLUMN approval_status TEXT DEFAULT 'Pending'
        """)
    except:
        pass

    conn.commit()

    conn.close()