import sqlite3

DB_NAME = "jobs.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        country TEXT,
        source TEXT,
        url TEXT,
        posted TEXT,
        status TEXT DEFAULT 'New'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        applied_date TEXT,
        status TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_sample_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

    sample = [
        ("Head of Sales","Google","Singapore","Demo","https://google.com","35 min ago","New"),
        ("Country Manager","Microsoft","Germany","Demo","https://microsoft.com","20 min ago","New"),
        ("VP Sales","Oracle","UAE","Demo","https://oracle.com","15 min ago","New"),
        ("Business Development Director","SAP","Poland","Demo","https://sap.com","55 min ago","New"),
        ("Chief Revenue Officer","Siemens","Saudi Arabia","Demo","https://siemens.com","45 min ago","New")
    ]

    cursor.executemany("""
        INSERT INTO jobs
        (title, company, country, source, url, posted, status)
        VALUES (?,?,?,?,?,?,?)
    """, sample)

    conn.commit()
    conn.close()

def get_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        title,
        company,
        country,
        source,
        posted,
        status
        FROM jobs
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

