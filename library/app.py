from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from sqlalchemy import or_
from forms import BookRequestForm, LoginForm, SearchForm, SignupForm
from models import db, User, Book, Loan
from werkzeug.security import generate_password_hash, check_password_hash

# Webアプリを作成し、appという変数に代入する
app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY_FOR_DEVELOPMENT"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap5(app)
db.init_app(app)
from handle_user import get_id, get_name, check_pw, is_id_dup, create_user


@app.route("/login", methods=["GET", "POST"])
def login():
    user_id = session.get("user_id")
    if user_id:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        print(f"name: {name}, get_id(): {get_id(name)}")
        if check_pw(name, form.password.data):
            session["user_id"] = get_id(name)
            flash("ログインに成功しました", "success")
            return redirect(url_for("index"))
        else:
            flash("ユーザIDまたはパスワードが間違っています", "danger")

    return render_template("login.html", form=form)


@app.route("/")
def index():
    id = session.get("user_id")
    if not id:
        return redirect(url_for("login"))
    today = datetime.now().strftime("%Y年%m月%d日")
    return_deadline = (datetime.now() + timedelta(weeks=2)).strftime("%Y年%m月%d日")

    return render_template(
        "index.html", today=today, return_deadline=return_deadline, user=get_name(id)
    )


request_list_data = []


@app.route("/request_book", methods=["GET", "POST"])
def request_book():
    id = session.get("user_id")
    if not id:
        return redirect(url_for("login"))

    from handle_request import add

    form = BookRequestForm()
    if form.validate_on_submit():
        add(form.title.data, form.author.data, form.reason.data)
        return redirect(url_for("request_list"))
    return render_template("request_form.html", form=form, user=get_name(id))


@app.route("/request_list")
def request_list():
    id = session.get("user_id")
    if not id:
        return redirect(url_for("login"))

    from handle_request import get_all

    request_list_data = get_all()

    return render_template(
        "request_list.html", requests=request_list_data, user=get_name(id)
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    id = session.get("user_id")
    if not id:
        return redirect(url_for("login"))

    from handle_search import search

    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        books = search(keyword)
        if not books:
            flash(f'"{keyword}" に一致する書籍は見付かりませんでした。', "info")
    else:
        books = []

    return render_template(
        "search.html", form=form, user=get_name(id), count=len(books), books=books
    )


@app.route("/borrow/<int:book_id>", methods=["POST"])
def borrow(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    current_user = User.query.get(user_id)

    book = Book.query.get_or_404(book_id)

    if book.is_borrowed:
        flash("この書籍はすでに貸出中です", "warning")
        return redirect(url_for("search"))

    loan = Loan(user=current_user, book=book)
    db.session.add(loan)
    db.session.commit()

    flash(f"「{book.title}」を借りました", "success")
    return redirect(url_for("borrowed_books"))

@app.route("/borrowed_books")
def borrowed_books():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    current_user = User.query.get(user_id)

    borrowed = Loan.query.filter_by(user=current_user, returned_at=None).all()

    return render_template('borrowed_books.html', borrowed=borrowed, user=current_user.username)

@app.route("/borrowed_history")
def borrowed_history():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    current_user = User.query.get(user_id)

    borrowed = Loan.query.filter_by(user=current_user).all()

    return render_template('borrowed_history.html', borrowed=borrowed, user=current_user.username)


@app.route("/return_book/<int:loan_id>", methods=['POST'])
def return_book(loan_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    current_user = User.query.get(user_id)

    # loan = Loan.query.get_or_404(loan_id)
    loan = Loan.query.filter_by(
        id=loan_id, user=current_user, returned_at=None
    ).first_or_404()
    if not loan:
        flash("貸出情報が見つかりりません", "warning")
        return redirect("borrowed_books")

    loan.returned_at = db.func.now()
    db.session.commit()

    flash(f"「{loan.book.title}」を返却しました", "success")

    return redirect(url_for('borrowed_books'))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    user_id = session.get("user_id")
    if user_id:
        return redirect(url_for("logout"))

    form = SignupForm()
    if form.validate_on_submit():
        name = form.username.data
        pw = form.password.data
        if is_id_dup(name):
            flash("希望ユーザIDは既に使用されています。別のIDを入力してください。", "warning")
        else:
            id = create_user(name, pw)
            session["user_id"] = id
            flash("サインアップに成功しました", "success")
            return redirect(url_for("index"))

    return render_template('signup.html', form=form)

    



# このファイルが直接実行された場合にサーバーを起動
if __name__ == "__main__":
    # debug=Trueにすると、コードを変更したときに自動で再起動される
    app.run(debug=True)
