from textblob import TextBlob
import sqlite3

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return round(analysis.sentiment.polarity, 2)

# Connect to the database
conn = sqlite3.connect('database/reviews.db')
c = conn.cursor()

# Loop through all reviews, calculate sentiment, and update the sentiment column
c.execute('SELECT rowid, review_text FROM reviews')
rows = c.fetchall()  # Fetch all rows to avoid issues with in-place updating

for row in rows:
    rowid, review_text = row
    polarity = analyze_sentiment(review_text)  # Calculate sentiment polarity
    c.execute('UPDATE reviews SET sentiment = ? WHERE rowid = ?', (polarity, rowid))
    conn.commit()  # Commit each update to ensure data integrity

# Close the connection after processing
conn.close()
