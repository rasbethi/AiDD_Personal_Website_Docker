import sqlite3

DB_NAME = 'projects.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()

    # Projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Ensure `link` column exists (for existing DBs)
    cols = conn.execute("PRAGMA table_info(projects)").fetchall()
    col_names = [c[1] for c in cols]
    if 'link' not in col_names:
        try:
            conn.execute("ALTER TABLE projects ADD COLUMN link TEXT")
        except Exception:
            pass

    # Project images table (for multiple images)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS project_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            imageFileName TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_project_with_images(title, description, imageFileNames, link=None):
    """Insert a project and multiple image filenames. Accepts optional link."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO projects (title, description, link) VALUES (?, ?, ?)',
        (title, description, link)
    )
    project_id = cursor.lastrowid

    for filename in imageFileNames:
        cursor.execute(
            'INSERT INTO project_images (project_id, imageFileName) VALUES (?, ?)',
            (project_id, filename)
        )

    conn.commit()
    conn.close()

def get_all_projects_with_images():
    """Fetch all projects and their associated images (including optional link)."""
    conn = get_db_connection()
    projects_data = conn.execute('SELECT * FROM projects').fetchall()

    projects = []
    for p in projects_data:
        images = conn.execute(
            'SELECT imageFileName FROM project_images WHERE project_id = ?',
            (p['id'],)
        ).fetchall()
        projects.append({
            'id': p['id'],
            'title': p['title'],
            'description': p['description'],
            'link': p['link'] if 'link' in p.keys() else None,
            'images': [img['imageFileName'] for img in images]
        })
    conn.close()
    return projects