import sqlite3

# Connect to the database file (creates database.db if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create a table for storing user data
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    graph_url TEXT NOT NULL
)
""")

# Save changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully!")
