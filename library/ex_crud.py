from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def create():
  with app.app_context():
    db.session.add(User(
      username = 'user2',
      password_hash = generate_password_hash('pass2')
    ))
    db.session.commit()

def read(key):
  with app.app_context():
    user = db.session.get(User, key)
    if user:
      print(f'Username: {user.username}')

def update(old, new):
  with app.app_context():
    user = User.query.filter(User.username == old).first()
    if user:
      user.username = new
      db.session.commit()

def delete(username):
  with app.app_context():
    user = User.query.filter(User.username == username).first()
    if user:
      db.session.delete(user)
      db.session.commit()

def read_all():
  with app.app_context():
    users = User.query.all()
    if len(users) > 0:
      for user in users:
        print(f'ID: {user.id}, Username: {user.username}')
      print('')


if __name__ == '__main__':
  # read(1) 
  read_all()
  create()
  read_all()
  update('user2', 'new-user')
  read_all()
  delete('new-user')
  read_all()