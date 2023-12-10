USE library;
DROP TABLE IF EXISTS books;
CREATE TABLE books (
    book_id INT AUTO_INCREMENT,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(100),
    publication_year INT,
    isbn VARCHAR(13),
    PRIMARY KEY(book_id)
);

-- Insert data for 10 books into the 'books' table
INSERT INTO books (title, author, genre, publication_year, isbn)
VALUES
    ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, '9780061120084'),
    ('1984', 'George Orwell', 'Dystopian', 1949, '9780451524935'),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925, '9780743273565'),
    ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 1951, '9780316769488'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, '9780141439518'),
    ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, '9780261102217'),
    ('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Fantasy', 1997, '9780747532743'),
    ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, '9780618640157'),
    ('The Alchemist', 'Paulo Coelho', 'Fiction', 1988, '9780062315007'),
    ('The Da Vinci Code', 'Dan Brown', 'Mystery', 2003, '9780307474278');
