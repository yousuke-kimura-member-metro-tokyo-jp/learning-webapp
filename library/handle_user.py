from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


def get_id(name):
    user = User.query.filter(User.username == name).first()
    if user:
        return user.id
    else:
        return None


def get_name(id):
    user = User.query.filter(User.id == id).first()
    if user:
        return user.username
    else:
        return None


def create_user(name, pw):
    db.session.add(User(username=name, password_hash=generate_password_hash(pw)))
    db.session.commit()
    return get_id(name)


def check_pw(name, pw):
    user = User.query.filter(User.username == name).first()
    if user:
        return check_password_hash(user.password_hash, pw)
    else:
        return None


def delete(username):
    user = User.query.filter(User.username == username).first()
    if user:
        db.session.delete(user)
        db.session.commit()


def is_id_dup(name):
    user = User.query.filter(User.username == name).first()
    if user:
        return True
    else:
        return False



if __name__ == "__main__":
    print(get_id("tama"))
