from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

book_author = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'))
)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(200))
    authors_of_book = db.relationship('Author', secondary=book_author , backref= db.backref('authors', lazy= 'dynamic'))
    book_copies = db.relationship('Book_copy', backref = 'book_item')

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(200))
    author_lastname = db.Column(db.String(200))

class Book_copy(db.Model):
    book_copy_id = db.Column(db.Integer, primary_key=True)
    publication_date = db.Column(db.Integer)
    book_item_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    book_loans = db.relationship('Book_loan', backref = 'book_loans_item')

class Book_loan(db.Model):
    book_loan_id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Integer)
    book_copy_loan_id = db.Column(db.Integer, db.ForeignKey('book_copy.book_copy_id'))


db.create_all()

"""
book1 = Book(book_title = 'Litte Miss Bossy')
book2 = Book(book_title = 'Litte Miss Naughty')
book3 = Book(book_title = 'Litte Miss Neat')
db.session.add(book1)
db.session.add(book2)
db.session.add(book3)
db.session.commit()
author1 = Author(author_name = 'Roger', author_lastname='Hargreaves')
author2 = Author(author_name = 'Lucy', author_lastname='Brown')
db.session.add(author1)
db.session.add(author2)
db.session.commit()
author1.authors.append(book1)
author1.authors.append(book2)
author2.authors.append(book2)
db.session.commit()
book4 = Book(book_title = 'Litte Miss SunshineNeat')
db.session.add(book4)
book1_copy_publ_date1 = Book_copy(publication_date=1985, book_item = book4)
book1_copy_publ_date2 = Book_copy(publication_date=1990, book_item = book4)
db.session.add(book1_copy_publ_date1)
db.session.add(book1_copy_publ_date2)
book1_loan_date1 = Book_loan(loan_date=2020, book_loans_item = book4)
book2_loan_date2 = Book_loan(loan_date=2010, book_Loans_item = book4)
db.session.add(book1_loan_date1)
db.session.add(book2_loan_date2)
db.session.commit()
"""
