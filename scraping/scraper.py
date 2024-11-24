import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Set up database connection
conn = sqlite3.connect('database/reviews.db')
c = conn.cursor()

# Function to insert review into the database, avoiding duplicates
def insert_review(title, review_text, style_name, color, verified_purchase, rating):
    c.execute('SELECT * FROM reviews WHERE title = ? AND review_text = ?', (title, review_text))
    if c.fetchone() is None:  # Only insert if review does not already exist
        c.execute('INSERT INTO reviews (title, review_text, style_name, color, verified_purchase, rating) VALUES (?, ?, ?, ?, ?, ?) ',
                  (title, review_text, style_name, color, verified_purchase, rating))
        conn.commit()

# Function to scrape reviews from a specific page
def scrape_reviews(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all review elements on the page
    reviews = soup.select('div[data-hook="review"]')

    for review in reviews:
        # Extract title, review text, style name, color, and verified purchase status
        title = review.select_one('a[data-hook="review-title"]').text.strip() if review.select_one('a[data-hook="review-title"]') else "No Title"
        review_text = review.select_one('span[data-hook="review-body"]').text.strip() if review.select_one('span[data-hook="review-body"]') else "No Text"
        
        # Extract style (storage size) and color
        style_info = review.select_one('a[data-hook="format-strip"]')
        style_name, color = "Unknown Storage", "Unknown Color"
        if style_info:
            style_info_text = style_info.text
            print(style_info_text)
            if "Size:" in style_info_text:
                style_name = style_info_text.split("Size: ")[-1].split("Pattern Name: ")[0]
            if "Colour:" in style_info_text:
                color = style_info_text.split("Colour: ")[-1].split("Size: ")[0]

        # Check if the review is marked as a verified purchase
        verified_purchase = "Yes" if review.select_one('span[data-hook="avp-badge"]') else "No"
        
        # Extract rating
        rating = review.select_one('i[data-hook="review-star-rating"]')
        rating_value = None
        if rating:
            rating_text = rating.text.strip()
            rating_value = float(rating_text.split(" ")[0])  # Convert to float

        # Insert review into the database
        insert_review(title, review_text, style_name, color, verified_purchase, rating_value)

# Loop through multiple pages of reviews
for i in range(1, 6):  # Adjust to scrape more pages as needed
    page_url = f"https://www.amazon.in/New-Apple-iPhone-12-128GB/product-reviews/B08L5TNJHG/?pageNumber={i}"
    scrape_reviews(page_url)
    time.sleep(2)  # Delay to avoid getting blocked by Amazon

conn.close()
