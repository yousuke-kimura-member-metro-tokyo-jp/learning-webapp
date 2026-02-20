# from flask import Flask
from models import db, BookRequest


def add(title, author, reason):
    db.session.add(BookRequest(title=title, author=author, reason=reason))
    db.session.commit()


def get_all():
    requests = BookRequest.query.all()
    return requests