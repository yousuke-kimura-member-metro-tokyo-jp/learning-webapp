# from flask import Flask
from models import db, Book
from sqlalchemy import or_


def search(keyword):
    # result_title = Book.query.filter(Book.title.like(f'%{keyword}%')).all()
    # result_author = Book.query.filter(Book.author.like(f'%{keyword}%')).all()
    # books = result_title + result_author

    books = Book.query.filter(
        or_(Book.title.like(f'%{keyword}%'), Book.author.like(f'%{keyword}%'))
    ).all()

    return books