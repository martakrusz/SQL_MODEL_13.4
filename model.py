from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Faker

#Faker.seed(0)
faker = Faker()

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

    title = db.Column(db.String(200))

    authors = db.relationship('Author', secondary=book_author , backref=db.backref('books', lazy='dynamic'))
    copies = db.relationship('BookCopy', backref='book')

    def __str__(self):
        return f"\"{self.title}\" {', '.join(map(str, sorted(self.authors, key=lambda author: author.last_name)))}"

class Author(db.Model):

    author_id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BookCopy(db.Model):

    book_copy_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))

    damaged = db.Column(db.Boolean, default=False)

    loans = db.relationship('BookLoan', backref='book_copy', lazy='dynamic')

    def __str__(self):
        return f"{self.book} [{'damaged' if self.damaged else 'available'}]"

class BookLoan(db.Model):

    book_loan_id = db.Column(db.Integer, primary_key=True)
    book_copy_id = db.Column(db.Integer, db.ForeignKey('book_copy.book_copy_id'))

    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    def __str__(self):
        return f"{self.loan_date} - {'?' if self.return_date is None else self.return_date}"

db.create_all()

authors = [
    Author(
        first_name=faker.first_name(),
        last_name=faker.last_name()
    ) for _ in range(10)
]

books = [
    Book(
        title=faker.catch_phrase(),
        authors=faker.random_choices(authors, faker.random_int(1, 3)),
        copies=[BookCopy(
            damaged=faker.boolean(chance_of_getting_true=10)
        ) for _ in range(faker.random_int(1, 5))]
    ) for _ in range(20)
]

db.session.add_all(authors)
db.session.add_all(books)
db.session.commit()

for copy in db.session.query(BookCopy).filter(BookCopy.damaged.is_(False)):
    copy.loans = [
        BookLoan(
            loan_date=faker.date_between(f'{2*n}w', f'{2*n+1}w'),
            return_date=faker.date_between(f'{2*n+1}w', f'{2*n+2}w')
        ) for n in range(-faker.random_int(2, 6), -1)
    ]
    if faker.boolean(chance_of_getting_true=25):
        copy.loans.append(BookLoan(loan_date=faker.date_between('-1w')))
    db.session.add(copy)
db.session.commit()

for book in db.session.query(Book).order_by(Book.title.asc()):
    for n, copy in enumerate(book.copies, 1):
        print(f'{n}/{len(book.copies)} - {copy}')
        for loan in copy.loans.order_by(BookLoan.loan_date.asc()):
            print(f' - {loan}')

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

#db.drop_all()
