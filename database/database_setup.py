import sqlite3

def create_database():
    conn = sqlite3.connect('database/reviews.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            title TEXT,
            review_text TEXT,
            style_name TEXT,
            color TEXT,
            verified_purchase TEXT,
            sentiment REAL,
            rating REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
