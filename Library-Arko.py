# Import necessary libraries/modules
from flask import Flask, jsonify, request  # Flask for web application, jsonify for JSON responses, request for handling HTTP requests
import mysql.connector  # Library to connect and interact with MySQL database
from flask_cors import CORS  # Flask extension for handling Cross-Origin Resource Sharing

# MySQL configurations - Contains database connection information
mysql_config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'Library',
    'database': 'library'
}

# Helper function to establish MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(**mysql_config)

# Create a Flask web application instance
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) for all routes in the application
CORS(app)

# Endpoint 1: Retrieve All Books (HTTP GET request)
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        # Establish a connection to the MySQL database
        conn = get_mysql_connection()
        cursor = conn.cursor()  # Create a cursor to execute SQL queries

        # Execute SQL query to select all books
        cursor.execute("SELECT * FROM books")

        # Fetch all book records from the query result
        books = cursor.fetchall()

        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        # Return JSON response with book data and HTTP status code 200
        return jsonify(books), 200

    except mysql.connector.Error as e:  # Handle MySQL-related errors
        return jsonify({'error': f"Database error: {e}"}), 500  # Return error response with HTTP status code 500

    except Exception as e:  # Handle other unexpected exceptions
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500  # Return error response with HTTP status code 500

# Endpoint 2: Add a New Book (HTTP POST request)
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        # Extract book details from the POST request JSON data
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_year = data.get('publication_year')
        isbn = data.get('isbn')

        # Validate if all necessary book details are provided
        if not all([title, author, genre, publication_year, isbn]):
            return jsonify({'error': 'Incomplete data provided'}), 400  # Return error response for incomplete data

        conn = get_mysql_connection()  # Establish a connection to the MySQL database
        cursor = conn.cursor()  # Create a cursor to execute SQL queries

        # Execute SQL query to insert new book details into the database
        cursor.execute("INSERT INTO books (title, author, genre, publication_year, isbn) VALUES (%s, %s, %s, %s, %s)",
                       (title, author, genre, publication_year, isbn))
        
        conn.commit()  # Commit the transaction to the database
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        # Return success message with HTTP status code 201 (created)
        return jsonify({'message': 'Book added successfully'}), 201

    except mysql.connector.IntegrityError as e:  # Handle integrity constraint violations (e.g., duplicate entry)
        return jsonify({'error': f"Duplicate entry. Book with ISBN {isbn} already exists"}), 400

    except Exception as e:  # Handle other unexpected exceptions
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500  # Return error response with HTTP status code 500

# Endpoint 3: Update Book Details (HTTP PUT request)
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book_details(book_id):
    try:
        # Extract updated book details from the PUT request JSON data
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_year = data.get('publication_year')
        isbn = data.get('isbn')

        conn = get_mysql_connection()  # Establish a connection to the MySQL database
        cursor = conn.cursor()  # Create a cursor to execute SQL queries

        # Execute SQL query to select a book based on its ID
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()  # Fetch the selected book record

        # If the book with the given ID doesn't exist, return a 404 error
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Execute SQL query to update book details in the database
        cursor.execute("UPDATE books SET title = %s, author = %s, genre = %s, publication_year = %s, isbn = %s WHERE book_id = %s",
                       (title, author, genre, publication_year, isbn, book_id))
        
        conn.commit()  # Commit the transaction to the database
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        # Return success message with HTTP status code 200
        return jsonify({'message': 'Book details updated successfully'}), 200

    except Exception as e:  # Handle other unexpected exceptions
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500  # Return error response with HTTP status code 500

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask application in debug mode
