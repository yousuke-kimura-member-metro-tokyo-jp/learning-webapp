from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"  # 慣習：クラス名を lowercase 化、複数化
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    loans = db.relationship("Loan", back_populates="user")


class BookRequest(db.Model):
    __tablename__ = "bookRequests"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=True)
    reason = db.Column(db.String(400), nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    loans = db.relationship("Loan", back_populates="book", lazy="dynamic")

    @property
    def is_borrowed(self):
        return self.loans.filter_by(returned_at=None).first() is not None


class Loan(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    borrowed_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    returned_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="loans")
    book = db.relationship("Book", back_populates="loans")