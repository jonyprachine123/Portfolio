import sqlite3
import os

# Path to the database file
db_path = 'instance/portfolio.db'

# Make sure the database exists
if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
    exit(1)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if youtube_url column exists in project table
cursor.execute("PRAGMA table_info(project)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# Add youtube_url column if it doesn't exist
if 'youtube_url' not in column_names:
    print("Adding youtube_url column to project table...")
    cursor.execute("ALTER TABLE project ADD COLUMN youtube_url TEXT")
    conn.commit()
    print("Added youtube_url column successfully.")
else:
    print("youtube_url column already exists.")

# Check if updated_at column exists in project table
if 'updated_at' not in column_names:
    print("Adding updated_at column to project table...")
    cursor.execute("ALTER TABLE project ADD COLUMN updated_at TIMESTAMP")
    conn.commit()
    print("Added updated_at column successfully.")
else:
    print("updated_at column already exists.")

# Create visitor table if it doesn't exist
print("Creating visitor table if it doesn't exist...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS visitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page TEXT,
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    visit_date DATE DEFAULT CURRENT_DATE
)
''')
conn.commit()
print("Visitor table created or already exists.")

# Close the connection
conn.close()
print("Database schema update completed successfully.")
