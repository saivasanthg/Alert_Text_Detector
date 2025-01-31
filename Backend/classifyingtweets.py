import sqlite3
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Path to the saved model folder
MODEL_PATH = "./results"  # Ensure this points to your 'results' folder

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Connect to SQLite database
conn = sqlite3.connect("tweets.db")
cursor = conn.cursor()

# Fetch all tweets that don't have classification yet
cursor.execute("SELECT tweet_id, content FROM tweets WHERE classification IS NULL")
tweets_to_classify = cursor.fetchall()

# Classify tweets and update the database
if tweets_to_classify:
    print(f"Found {len(tweets_to_classify)} tweets to classify. Processing...")
    for tweet_id, content in tweets_to_classify:
        # Tokenize the tweet
        inputs = tokenizer(content, return_tensors="pt", padding=True, truncation=True, max_length=128)

        # Predict classification
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            classification = "alert" if torch.argmax(logits, dim=1).item() == 1 else "regular"

        # Update database with classification
        cursor.execute("UPDATE tweets SET classification=? WHERE tweet_id=?", (classification, tweet_id))

    # Commit changes to the database
    conn.commit()
    print(f"Classified {len(tweets_to_classify)} tweets and updated the database!")
else:
    print("No tweets found for classification.")

# Fetch and display updated tweets
cursor.execute("SELECT tweet_id, content, classification FROM tweets")
classified_tweets = cursor.fetchall()

print("\nClassified Tweets:")
for tweet_id, content, classification in classified_tweets:
    print(f"Tweet ID: {tweet_id}")
    print(f"Content: {content}")
    print(f"Classification: {classification}")
    print("-" * 40)

# Close connection
conn.close()
