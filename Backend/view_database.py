import sqlite3

def view_database():
    # Connect to SQLite database
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()

    # Fetch data from the 'users' table
    print("=== Users Table ===")
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    for user in users:
        print(user)

    # Fetch data from the 'tweets' table
    print("\n=== Tweets Table ===")
    cursor.execute("SELECT * FROM tweets;")
    tweets = cursor.fetchall()
    for tweet in tweets:
        print(tweet)

    # Close the connection
    conn.close()

# Call the function to view the database
if __name__ == "__main__":
    view_database()
