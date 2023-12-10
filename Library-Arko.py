from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS  # Import CORS from flask_cors

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'port':'3306',
    'user': 'root',
    'password': 'Library',
    'database': 'library'
}

# Helper function to establish MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(**mysql_config)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        return jsonify(books), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_year = data.get('publication_year')
        isbn = data.get('isbn')

        if not title or not author or not genre or not publication_year or not isbn:
            return jsonify({'error': 'Incomplete data provided'}), 400

        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Insert the record, and ignore if a duplicate key error occurs (assuming isbn is a unique key)
        cursor.execute("INSERT IGNORE INTO books (title, author, genre, publication_year, isbn) VALUES (%s, %s, %s, %s, %s)",
                       (title, author, genre, publication_year, isbn))
        
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Book added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint 3: Update Book Details
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book_details(book_id):
    try:
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_year = data.get('publication_year')
        isbn = data.get('isbn')

        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({'error': 'Book not found'}), 404

        cursor.execute("UPDATE books SET title = %s, author = %s, genre = %s, publication_year = %s, isbn = %s WHERE book_id = %s",
                       (title, author, genre, publication_year, isbn, book_id))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Book details updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
