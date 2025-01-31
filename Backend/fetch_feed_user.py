import sqlite3

# Connect to the database
conn = sqlite3.connect("tweets.db")
cursor = conn.cursor()

def fetch_user_feed(user_id):
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

    # Debugging: print out regular tweets
    print("Regular Tweets Matching Interests:")
    for tweet in regular_tweets:
        print(tweet)

    # Fetch alert tweets matching location
    alert_tweets = cursor.execute("""
        SELECT * FROM tweets
        WHERE classification='alert' AND location=?
    """, (location,)).fetchall()

    return {"regular_tweets": regular_tweets, "alert_tweets": alert_tweets}

# Fetch feed for all users
cursor.execute("SELECT user_id FROM users")
user_ids = cursor.fetchall()

# Loop through all user IDs and fetch their feed
all_user_feeds = {}
for user_id_tuple in user_ids:
    user_id = user_id_tuple[0]
    feed = fetch_user_feed(user_id)
    all_user_feeds[user_id] = feed

# Print the feeds for all users
for user_id, feed in all_user_feeds.items():
    print(f"\nUser ID: {user_id}")
    print(f"Feed: {feed}")

# Close connection
conn.close()
