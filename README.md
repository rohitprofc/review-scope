# ReviewScope

ReviewScope is a Python-based project that scrapes product reviews from Amazon, performs sentiment analysis on them, and provides APIs for retrieving and analyzing the reviews. This project is structured to facilitate web scraping, database storage, sentiment analysis, and API integration, making it a versatile tool for review-based insights.

## Features
- **Web Scraping**: Scrapes product reviews from Amazon, including details like title, review text, storage size, color, and verified purchase status.
- **Sentiment Analysis**: Analyzes review sentiments using TextBlob to identify positive and negative sentiments in customer feedback.
- **APIs**: Provides two APIs:
  - **Sentiment Analysis API**: Analyzes the sentiment of a new review.
  - **Review Retrieval API**: Fetches reviews based on specific filters like color and storage size.

## Project Structure
```plaintext
project_name/
├── app.py                    # Main Flask application containing API endpoints
├── requirements.txt          # List of dependencies for the project
├── README.md                 # Project description and instructions
├── database/
│   └── reviews.db            # SQLite database file to store scraped reviews
├── scraping/
│   ├── scraper.py            # Script for scraping Amazon reviews and saving them to the database
│   └── database_setup.py      # Script for setting up the database schema
├── sentiment_analysis/
│   └── analyze_sentiment.py   # Script to perform sentiment analysis on reviews
└── utils/
    └── helpers.py            # Utility functions (e.g., for sentiment analysis, database connection)
```

## Getting Started

### Prerequisites
- Python 3.8+
- Recommended libraries (install via `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ReviewScope.git
   cd ReviewScope
   ```

2. **Set up the database**:
   ```bash
   python scraping/database_setup.py
   ```

3. **Run the scraper** to populate the database:
   ```bash
   python scraping/scraper.py
   ```

4. **Perform sentiment analysis**:
   ```bash
   python sentiment_analysis/analyze_sentiment.py
   ```

5. **Start the API server**:
   ```bash
   python app.py
   ```

## Usage

### Scraping Reviews
The `scraper.py` script scrapes Amazon reviews for a specific product and saves them in the SQLite database. Adjust the page count in `scraper.py` to control how many pages of reviews are scraped.

### Sentiment Analysis
Run `analyze_sentiment.py` to perform sentiment analysis on each review stored in the database. Sentiment scores are saved in the database for easy retrieval.

### API Endpoints

- **Sentiment Analysis API**
  - **Endpoint**: `POST /analyze`
  - **Description**: Accepts a review and returns the sentiment score.
  - **Request**:
    ```json
    {
      "review": "This is an amazing product!"
    }
    ```
  - **Response**:
    ```json
    {
      "sentiment": 0.8
    }
    ```

- **Review Retrieval API**
  - **Endpoint**: `GET /reviews`
  - **Description**: Retrieves reviews based on filters such as color and storage size.
  - **Query Parameters**:
    - `color`: The color of the product.
    - `storage`: The storage size of the product.
  - **Example Request**:
    ```
    GET /reviews?color=Black&storage=128GB
    ```
  - **Response**:
    ```json
    [
      {
        "title": "Great phone!",
        "review_text": "The iPhone 12 is fantastic.",
        "style_name": "128GB",
        "color": "Black",
        "verified_purchase": "Yes",
        "sentiment": 0.7
      },
      ...
    ]
    ```

## File Overview

- **`app.py`**: Contains the Flask app and API routes.
- **`database_setup.py`**: Sets up the SQLite database and schema for storing reviews.
- **`scraper.py`**: Script to scrape Amazon reviews and store them in the database.
- **`analyze_sentiment.py`**: Analyzes the sentiment of each review and saves it in the database.
- **`helpers.py`**: Contains utility functions for sentiment analysis and database connections.

## Troubleshooting

- **Amazon Blocking**: If Amazon detects scraping, try using a proxy or adding delays.
- **Database Errors**: Ensure the database is set up properly by running `database_setup.py` before scraping.
- **API Testing**: Use tools like **Postman** to test the APIs.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
