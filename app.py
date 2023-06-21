from flask import request, redirect, render_template,Flask,flash,session,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, BLOB
import base64
from werkzeug.security import generate_password_hash
from flask_login import current_user
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from io import BytesIO

app = Flask(__name__)
app.secret_key ='123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/bukubook'
db = SQLAlchemy(app)

library_books = db.Table('library_books',
    db.Column('library_id', db.Integer, db.ForeignKey('library.id'), primary_key=True),
    db.Column('book_id', db.String(30), db.ForeignKey('book.id'), primary_key=True)
)

def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')

app.jinja_env.filters['decode_base64'] = decode_base64

class Book(db.Model):
    __tablename__ = 'book'

    id = Column(String(30), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), nullable=False)
    categories = Column(String(30), nullable=False)
    rate = Column(Integer, nullable=False)
    cover = Column(BLOB, nullable=False)
    pdf = Column(BLOB, nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    user_name = Column(db.String(30), primary_key=True)
    email = Column(db.String(50), nullable=False)
    password = Column(db.String(16), nullable=False)
    library = relationship('Library', backref='user', uselist=False, cascade="all, delete")
    is_admin = Column(db.Boolean, default=False)

class Library(db.Model):
    __tablename__ = 'library'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), nullable=False)
    categories = Column(String(30), nullable=False)
    rate = Column(Integer, nullable=False)
    cover = Column(BLOB, nullable=False)
    pdf = Column(BLOB, nullable=False)
    user_name = Column(db.String(30), db.ForeignKey('user.user_name'), nullable=False)

@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)

@app.route('/top_books')
def top_books():
    books = Book.query.all()
    return render_template('top books.html', books=books, base64=base64)
@app.route('/categories', methods=['GET'])
def categories():
    categories = db.session.query(Book.categories.distinct()).all()
    return render_template('Categories.html', categories=categories)

@app.route('/books_by_category', methods=['GET'])
def books_by_category():
    categories = request.args.get('category')
    books = Book.query.filter(Book.categories == categories).all()
    return render_template('filtred_books.html', books=books, base64=base64)
@app.route('/authors', methods=['GET'])
def authors():
    search_query = request.args.get('search')
    sort_order = request.args.get('sort')
    if search_query:
        search_query = search_query.lower()
        matched_authors = Book.query.filter(Book.author.ilike(f'%{search_query}%')).all()
        authors = list(set([author.author for author in matched_authors]))  
        selected_author = search_query.lower()   
    else:
        authors = list(set([author.author for author in Book.query.all()]))  
        selected_author = None
    if sort_order == 'asc':
        authors.sort()
    elif sort_order == 'desc':
        authors.sort(reverse=True)

    return render_template('authors.html', authors=authors, selected_author=selected_author)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('register.html')
        
        new_user = User(user_name=user_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        

    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(user_name=username).first()

        if user and user.password == password:
            session['username'] = user.user_name  
            flash('Login successful!', 'success')
            if user.is_admin: 
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            flash('Invalid username or password.', 'error')
    if 'username' in session:
        return redirect('/')
    
    return render_template('login.html')

@app.route('/private-library', methods=['GET'])
def private_library():
    if 'username' not in session:
        return redirect('/login')

    user_name = session['username']
    user = User.query.get(user_name)

    if user:
        books = Library.query.filter_by(user_name=user_name).all()
        return render_template('private_lib.html', user=user, books=books,base64=base64)
    else:
        return redirect('/')

@app.route('/user/books/create', methods=['GET', 'POST'])
def create_user_book():
    if 'username' not in session:
        return redirect('/login')

    user_name = session['username']
    user = User.query.get(user_name)

    if user:
        if request.method == 'POST':
            id = request.form['ISBN']
            title = request.form['title']
            author = request.form['author']
            categories = request.form['categories']
            rate = float(request.form['rate'])
            cover = request.files['cover']
            pdf = request.files['pdf']

            new_book = Library(id=id, title=title, author=author, categories=categories, rate=rate, cover=cover.read(), pdf=pdf.read(), user_name=user_name)

            db.session.add(new_book)
            db.session.commit()

            flash('Book created successfully!', 'success')
            return redirect('/private-library')

        return render_template('user_create_book.html')
    else:
        return redirect('/')
from flask import Flask, render_template, request, redirect, url_for, flash

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'username' in session:
        book_id = request.form.get('book_id')
        
        book = Book.query.get(book_id)
        
        if book is None:
            flash('Book not found', 'error')
            return redirect(url_for('private_library'))

        library_book = Library()

        library_book.id = book.id
        library_book.title = book.title
        library_book.author = book.author
        library_book.categories = book.categories
        library_book.rate = book.rate
        library_book.cover = book.cover
        library_book.pdf = book.pdf
        
        library_book.user_name = session['username']
        
        try:
            db.session.add(library_book)
            db.session.commit()
        except IntegrityError:
            flash('This book already exists in your library!', 'error')
            db.session.rollback()
        
        return redirect(url_for('private_library'))
    else:
        return redirect(url_for('login'))




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session:
        return redirect('/login')

    user_name = session['username']
    user = User.query.get(user_name)

    if user and user.is_admin:
        books = Book.query.all()
        return render_template('admin_dashboard.html', books=books)
    else:
        return redirect('/')



@app.route('/base')
def base():
    return render_template('base.html', current_user=current_user)


@app.route('/admin/books/create', methods=['GET', 'POST'])
def create_book():
    if 'username' not in session:
        return redirect('/login')

    user_name = session['username']
    user = User.query.get(user_name)

    if user and user.is_admin:
        if request.method == 'POST':
            id = request.form['ISBN']
            title = request.form['title']
            author = request.form['author']
            categories = request.form['categories']
            rate = float(request.form['rate'])
            cover = request.files['cover']
            pdf = request.files['pdf']

            existing_book = Book.query.filter_by(id=id).first()
            if existing_book:
                flash('This book already exists!', 'error')
                return redirect('/admin/books/create')

            new_book = Book(
                id=id,
                title=title,
                author=author,
                categories=categories,
                rate=rate,
                cover=cover.read(),
                pdf=pdf.read()
            )

            db.session.add(new_book)
            db.session.commit()

            flash('Book created successfully!', 'success')
            return redirect('/admin')

        return render_template('admin_create_book.html')
    else:
        return redirect('/')

# Update an existing book
@app.route('/admin/books/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    if 'username' not in session:
        return redirect('/login')
    
    user_name = session['username']
    user = User.query.get(user_name)
    
    if user and user.is_admin:
        book = Book.query.get(book_id)
        
        if not book:
            flash('Book not found.', 'error')
            return redirect('/admin/books')
        
        if request.method == 'POST':
            book.title = request.form['title']
            book.author = request.form['author']
            book.categories = request.form['categories']
            book.rate = float(request.form['rate'])
            
            cover = request.files['cover']
            if cover.filename:
                book.cover = cover.read()
            
            pdf = request.files['pdf']
            if pdf.filename:
                book.pdf = pdf.read()
            
            db.session.commit()
            
            flash('Book updated successfully!', 'success')
            return redirect('/admin')
        
        return render_template('admin_update_book.html', book=book)
    else:
        return redirect('/')

@app.route('/admin/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'username' not in session:
        return redirect('/login')
    
    user_name = session['username']
    user = User.query.get(user_name)
    
    if user and user.is_admin:
        book = Book.query.get(book_id)
        
        if not book:
            flash('Book not found.', 'error')
            return redirect('/admin/books')
        
        db.session.delete(book)
        db.session.commit()
        
        flash('Book deleted successfully!', 'success')
        return redirect('/admin')
    else:
        return redirect('/')



@app.route('/admin/users')
def admin_users():
    if 'username' not in session:
        return redirect('/login')
    
    user_name = session['username']
    user = User.query.get(user_name)
    
    users = []
    
    if user and user.is_admin:
        users = User.query.all()
    else:
        return redirect('/')

    return render_template('admin_users.html', users=users)


@app.route('/admin/users/create', methods=['GET', 'POST'])
def admin_create_user():
    if 'username' not in session:
        return redirect('/login')

    user_name = session['username']
    user = User.query.get(user_name)
    
    if not user or not user.is_admin:
        return redirect('/')

    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form

        new_user = User(user_name=user_name, email=email, password=password, is_admin=is_admin)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/admin/users')
    
    return render_template('admin_create_user.html')


@app.route('/admin/users/edit/<user_name>', methods=['GET', 'POST'])
def admin_edit_user(user_name):
    if 'username' not in session:
        return redirect('/login')

    admin_user = User.query.get(session['username'])
    if not admin_user or not admin_user.is_admin:
        return redirect('/')

    user = User.query.get(user_name)
    if not user:
        return redirect('/admin/users')

    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['password']
        user.is_admin = 'is_admin' in request.form

        db.session.commit()

        return redirect('/admin/users')

    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/users/delete/<user_name>', methods=['POST'])
def admin_delete_user(user_name):
    user = User.query.get(user_name)
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/admin/users')

@app.route('/download_pdf/<book_id>')
def download_pdf(book_id):
    if 'username' in session:
        library_book = Library.query.filter_by(id=book_id, user_name=session['username']).first()
        
        if library_book is None:
            flash('Book not found', 'error')
            return redirect(url_for('private_library'))
        
        pdf_data = library_book.pdf
        
        return send_file(BytesIO(pdf_data), mimetype='application/pdf', download_name='book.pdf')
    else:
        return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
