import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("tweets.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    interests TEXT,
    location TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    tweet_id INTEGER PRIMARY KEY,
    content TEXT,
    location TEXT,
    classification TEXT,
    genre TEXT
);
""")

# Populate users table
users = [
    (1, "user1", "sports", "Bengaluru"),
    (2, "user2", "technology", "Hyderabad"),
    (3, "user3", "movies", "Lucknow"),
    (4, "user4", "politics", "Mumbai")
]

cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?);", users)

# Populate tweets table with new data
tweets = [
    (101, "Breaking news: A sandstorm is coming!", "Jaipur", "alert", None),
    (102, "Huge accident in Habsiguda area! A truck collided with the divider.", "Hyderabad", "alert", None),
    (103, "Thoroughly enjoyed Avatar 2", "Mumbai", "regular", "entertainment"),
    (104, "I just got rejected by Infosys", "New Delhi", "regular", "personal"),
    (105, "The stock market just crashed! Take precautions.", "Bengaluru", "alert", "finance"),
    (106, "Upcoming IPL match scheduled between Chennai and Mumbai", "Chennai", "regular", "sports"),
    (107, "Political unrest in Mumbai, protests ongoing.", "Mumbai", "alert", "politics"),
    (108, "I would any day prefer Android over Apple", "Lucknow", "regular", "technology"),
    (109, "Stock market prices continue to plummet in major cities.", "Hyderabad", "alert", "finance"),
    (110, "Excited about the upcoming tech conference next month.", "Bengaluru", "regular", "technology"),
    (111, "Just watched the latest Spider-Man movie and loved it!", "Mumbai", "regular", "movies"),
    (112, "Political unrest in some regions, tensions are rising.", "Chennai", "alert", "politics"),
    (113, "New Android update is out with some amazing features.", "Lucknow", "regular", "technology"),
    (114, "It's the weekend! Time to catch up on some movies.", "Lucknow", "regular", "movies"),
    (115, "Urgent: Protests have broken out in several locations.", "Hyderabad", "alert", "politics"),
    (116, "Have you heard about the latest on electric vehicle technology?", "Mumbai", "regular", "technology"),
    (117, "Big political rally happening in Delhi today.", "New Delhi", "alert", "politics"),
    (118, "I'm planning a trip to Europe in the summer. Excited!", "Bengaluru", "regular", "personal"),
    (119, "IPL cricket tournament is heating up!", "Chennai", "regular", "sports"),
    (120, "Breaking news: Power outage reported in several cities!", "Mumbai", "alert", None),
    (121, "The economy is looking better despite global challenges.", "Mumbai", "regular", "finance"),
    (122, "An update on the latest electric car sales figures.", "Hyderabad", "regular", "technology"),
    (123, "Severe weather warning in place for coastal areas.", "Chennai", "alert", None),
    (124, "Movie night with friends, can't wait to watch a classic!", "Lucknow", "regular", "movies"),
]


cursor.executemany("INSERT OR IGNORE INTO tweets VALUES (?, ?, ?, ?, ?);", tweets)

# Commit and close
conn.commit()
print("Database created and populated successfully with new tweets including genres!")
conn.close()
