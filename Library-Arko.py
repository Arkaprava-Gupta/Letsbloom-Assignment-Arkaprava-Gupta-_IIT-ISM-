from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Database configurations
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Library@localhost:3306/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define a model for Book
class
 
Book(db.Model):
    __tablename__ = "books"


    
id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50))
    publication_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

CORS(app)

# Endpoint 1: Retrieve All Books (GET)
@app.route("/api/books", methods=["GET"])
def get_all_books():
    books = Book.query.all()
    return jsonify({"books": [book.serialize() for book in books]})

# Endpoint 2: Add a New Book (POST)
@app.route("/api/books", methods=["POST"])
def add_new_book():
    data = request.json
    if not all(key in data for key in ("title", "author", "publication_year", "isbn")):
        abort(400, description="Missing required fields.")

    try:
        book = Book(
            title=data["title"],
            author=data["author"],
            genre=data.get("genre"),
            publication_year=data["publication_year"],
            isbn=data["isbn"],
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book added successfully."}), 201
    except Exception as e:
        abort(400, description=str(e))

# Endpoint 3: Update Book Details (PUT)
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book_details(book_id):
    data = request.json
    if not any(data):
        abort(400, description="No data provided for update.")

    try:
        book = Book.query.get(book_id)
        if not book:
            abort(404, description="Book not found.")

        for key, value in data.items():
            setattr(book, key, value)

        db.session.commit()
        return jsonify({"message": "Book details updated successfully."}), 200
    except Exception as e:
        abort(400, description=str(e))

# Serialization helper
def serialize(self):
    return {
        "id": self.id,
        "title": self.title,
        "author": self.author,
        "genre": self.genre,
        "publication_year": self.publication_year,
        "isbn": self.isbn,
    }

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
