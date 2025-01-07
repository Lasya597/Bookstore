# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# import subprocess
# import os

# app = Flask(__name__)

# # Database connection
# def get_db_connection():
#     conn = sqlite3.connect('books.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Check if the books table exists
# def table_exists():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT name 
#         FROM sqlite_master 
#         WHERE type='table' AND name='books';
#     """)
#     result = cursor.fetchone()
#     conn.close()
#     return result is not None

# # Run books_db.py if the table doesn't exist
# def initialize_database():
#     if not table_exists():
#         print("Table 'books' not found. Running books_db.py...")
#         subprocess.run(["python", "books_db.py"], check=True)
#     else:
#         print("Table 'books' already exists. Continuing...")

# # Home Page
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     books = conn.execute('SELECT * FROM books').fetchall()
#     conn.close()
#     return render_template('index.html', books=books)

# # Add a Book
# @app.route('/add', methods=('GET', 'POST'))
# def add_book():
#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         price = request.form['price']
        
#         conn = get_db_connection()
#         conn.execute('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', (title, author, price))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('index'))
#     return render_template('add_book.html')

# # Edit a Book
# @app.route('/edit/<int:book_id>', methods=('GET', 'POST'))
# def edit_book(book_id):
#     conn = get_db_connection()
#     book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         price = request.form['price']

#         conn.execute('UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?',
#                      (title, author, price, book_id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('index'))

#     conn.close()
#     return render_template('edit_book.html', book=book)

# # Delete a Book
# @app.route('/delete/<int:book_id>', methods=('POST',))
# def delete_book(book_id):
#     conn = get_db_connection()
#     conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('index'))

# # Contact Us Page
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# # About Us Page
# @app.route('/about')
# def about():
#     return render_template('about.html')

# if __name__ == '__main__':
#     initialize_database()
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import subprocess

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# Check if the books table exists
def table_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='books';
    """)
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Run books_db.py if the table doesn't exist
def initialize_database():
    if not table_exists():
        print("Table 'books' not found. Running books_db.py...")
        try:
            subprocess.run(["python", "books_db.py"], check=True)
            print("Database initialized successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running books_db.py: {e}")
            exit(1)  # Exit if the database initialization fails
    else:
        print("Table 'books' already exists. Continuing...")

# Home Page
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add a Book
@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', (title, author, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Edit a Book
@app.route('/edit/<int:book_id>', methods=('GET', 'POST'))
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']

        conn.execute('UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?',
                     (title, author, price, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_book.html', book=book)

# Delete a Book
@app.route('/delete/<int:book_id>', methods=('POST',))
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Contact Us Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# About Us Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    initialize_database()  # Ensure the database is ready before running the app
    app.run(debug=True)
