from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

books = Blueprint('books', __name__)


@books.route('/book', methods=['GET', 'POST'])
def book():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new book
    if request.method == 'POST':
        title = request.form['book_title']
        genre = request.form['genre']
        description = request.form['description']
        cover_image = request.form['cover_image']

        # Insert the new runner into the database
        cursor.execute('INSERT INTO books (title, genre, description, cover_image) VALUES (%s, %s, %s, %s)', (title, genre, description, cover_image))
        db.commit()

        flash('New book added successfully!', 'success')
        return redirect(url_for('books.book'))

    # Handle GET request to display all books
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    return render_template('books.html', all_books=all_books)


@books.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the book's details
        title = request.form['book_title']
        genre = request.form['genre']
        description = request.form['description']
        cover_image = request.form['cover_image']

        cursor.execute('UPDATE books SET title = %s, genre = %s, description = %s, cover_image = %s WHERE book_id = %s',
                       (title, genre, description, cover_image, book_id))
        db.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book'))

    # GET method: fetch book's current data for pre-populating the form
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    single_book = cursor.fetchone()
    return render_template('update_book.html', book=single_book)


@books.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the book
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    db.commit()

    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books.book'))
