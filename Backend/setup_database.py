import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("tweets.db")
cursor = conn.cursor()

# Create 'users' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT,
    interests TEXT
);
""")

# Create 'tweets' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    tweet_id INTEGER PRIMARY KEY,
    content TEXT,
    location TEXT,
    classification TEXT
);
""")

conn.commit()
print("Database and tables created.")
conn.close()
