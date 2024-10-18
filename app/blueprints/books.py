from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

books = Blueprint('books', __name__)


@books.route('/book', methods=['GET', 'POST'])
def book():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new book
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        description = request.form['description']
        cover_image = request.form['cover_image']

        # Insert the new book into the database
        cursor.execute('INSERT INTO books (title, genre, description, cover_image) VALUES (%s, %s, %s, %s)', (title, genre, description, cover_image))
        db.commit()

        flash('New book added successfully!', 'success')
        return redirect(url_for('books.book'))

    # Handle GET request to display all books
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    return render_template('books.html', all_books=all_books)

# Add a new route to handle author data
@books.route('/authors', methods=['GET', 'POST'])
def author():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new book
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']

        # Insert the new author into the database
        cursor.execute('INSERT INTO authors (name, bio) VALUES (%s, %s)', (name, bio))
        db.commit()

        flash('New author added successfully!', 'success')
        return redirect(url_for('books.author'))

    # Handle GET request to display all authors
    cursor.execute('SELECT * FROM authors')
    all_authors = cursor.fetchall()
    return render_template('authors.html', all_authors=all_authors)


@books.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the book's details
        title = request.form['title']
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
    book = cursor.fetchone()
    return render_template('update_book.html', book=book)

# Add a new route to update author data
@books.route('/update_author/<int:author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the author's details
        name = request.form['name']
        bio = request.form['bio']

        cursor.execute('UPDATE authors SET name = %s, bio = %s WHERE author_id = %s',
                       (name, bio, author_id))
        db.commit()

        flash('Author updated successfully!', 'success')
        return redirect(url_for('books.author'))

    # GET method: fetch author's current data for pre-populating the form
    cursor.execute('SELECT * FROM authors WHERE author_id = %s', (author_id,))
    author = cursor.fetchone()
    return render_template('update_author.html', author=author)


@books.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the book
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    db.commit()

    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books.book'))

# Add a new route to delete author data
@books.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the book
    cursor.execute('DELETE FROM authors WHERE author_id = %s', (author_id,))
    db.commit()

    flash('Author deleted successfully!', 'danger')
    return redirect(url_for('books.author'))
