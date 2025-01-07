# import sqlite3

# connection = sqlite3.connect('books.db')

# with connection:
#     connection.execute("""
#         CREATE TABLE books (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             author TEXT NOT NULL,
#             price REAL NOT NULL
#         );
#     """)

# connection.close()
# print("Database and table created successfully!")


#https://onlinebookstore-30e82-default-rtdb.firebaseio.com/

import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("Credentials.json")
    firebase_admin.initialize_app(cred,{'databaseURL':'https://onlinebookstore-30e82-default-rtdb.firebaseio.com/'})
    return firestore.client()

# Synchronize SQLite data to Firebase
def sync_to_firebase(db_connection, firestore_client):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    for book in books:
        book_id, title, author, price = book
        firestore_client.collection('books').document(str(book_id)).set({
            'title': title,
            'author': author,
            'price': price
        })
    print("Data synchronized to Firebase successfully!")

# Create SQLite database and table
def create_sqlite_db():
    connection = sqlite3.connect('books.db')
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                price REAL NOT NULL
            );
        """)
    print("Database and table created successfully!")
    return connection

# Main workflow
if __name__ == "__main__":
    # Step 1: Create SQLite DB and Table
    sqlite_connection = create_sqlite_db()

    try:
        # Step 2: Initialize Firebase
        firestore_client = initialize_firebase()

        # Step 3: Add sample data to SQLite (optional, if no data exists)
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            sqlite_connection.executemany("""
                INSERT INTO books (title, author, price) VALUES (?, ?, ?)
            """, [
                ('Book 1', 'Author 1', 19.99),
                ('Book 2', 'Author 2', 25.50),
                ('Book 3', 'Author 3', 14.75)
            ])
            sqlite_connection.commit()
            print("Sample data inserted successfully!")

        # Step 4: Synchronize SQLite data to Firebase
        sync_to_firebase(sqlite_connection, firestore_client)
    finally:
        # Ensure the SQLite connection is closed after all operations
        sqlite_connection.close()
        print("SQLite connection closed.")
