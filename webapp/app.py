from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def fetch_user_feed(user_id):
    # Connect to SQLite database
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()

    # Fetch user details
    user = cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    if not user:
        return "User not found."
    
    location, interests = user[3], user[2].split(',')
    print(f"User Interests: {interests}")  # Debugging

    # Fetch regular tweets matching interests
    placeholders = ', '.join(['?'] * len(interests))
    regular_tweets = cursor.execute(f"""
        SELECT * FROM tweets
        WHERE classification='regular' AND genre IN ({placeholders})
    """, interests).fetchall()

    # Fetch alert tweets matching location
    alert_tweets = cursor.execute(""" 
        SELECT * FROM tweets
        WHERE classification='alert' AND location=?
    """, (location,)).fetchall()

    conn.close()
    return {"regular_tweets": regular_tweets, "alert_tweets": alert_tweets}

def fetch_all_user_feeds():
    # Connect to the database
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()

    # Fetch all user IDs
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()

    # Loop through all user IDs and fetch their feed
    all_user_feeds = {}
    for user_id_tuple in user_ids:
        user_id = user_id_tuple[0]
        feed = fetch_user_feed(user_id)
        all_user_feeds[user_id] = feed

    conn.close()
    return all_user_feeds

@app.route('/')
def index():
    # Fetch all user feeds
    all_user_feeds = fetch_all_user_feeds()
    return render_template('index.html', all_user_feeds=all_user_feeds)

if __name__ == "__main__":
    app.run(debug=True)
