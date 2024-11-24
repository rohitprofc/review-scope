from flask import Flask, request, jsonify, render_template
from utils.helpers import analyze_sentiment
import sqlite3

app = Flask(__name__)

# Home route to render the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Sentiment Analysis API
@app.route('/analyze', methods=['POST'])
def sentiment_analysis():
    data = request.json
    review = data.get('review', '')
    if not review:
        return jsonify({'error': 'Review text is required'}), 400

    polarity = analyze_sentiment(review)
    rounded_polarity = round(polarity, 2)  # Round to 2 decimal places
    return jsonify({'sentiment': rounded_polarity})

# Review Retrieval API
@app.route('/reviews', methods=['GET'])
# Review Retrieval API
@app.route('/reviews', methods=['GET'])
def get_reviews():
    color = request.args.get('color')
    storage = request.args.get('storage')
    rating = request.args.get('rating')
    
    conn = sqlite3.connect('database/reviews.db')
    c = conn.cursor()
    
    # Build the query dynamically based on the provided filters
    query = "SELECT * FROM reviews WHERE 1=1"  # Base query
    params = []
    
    if color:
        query += " AND color = ?"
        params.append(color)
    if storage:
        query += " AND style_name = ?"
        params.append(storage)
    if rating:
        query += " AND rating = ?"
        params.append(rating)

    c.execute(query, params)
    reviews = [{'title': row[0], 'review_text': row[1], 'style_name': row[2], 'color': row[3], 'verified_purchase': row[4], 'sentiment': row[5], 'rating': row[6]} for row in c.fetchall()]
    conn.close()
    
    return jsonify(reviews)



if __name__ == '__main__':
    app.run(debug=True)
