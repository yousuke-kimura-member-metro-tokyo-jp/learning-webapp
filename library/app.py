from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm

# Webアプリを作成し、appという変数に代入する
app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY_FOR_DEVELOPMENT"

Bootstrap5(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == "tamapass" and form.username.data == "tama":
            flash("ログインに成功しました", "success")
            return redirect(url_for("index"))
        else:
            flash("ユーザIDまたはパスワードが間違っています", "danger")

    return render_template("login.html", form=form)

@app.route('/')
def index():    
    today = datetime.now().strftime("%Y年%m月%d日")
    return_deadline = (datetime.now() + timedelta(weeks=2)).strftime("%Y年%m月%d日")
    
    return render_template("index.html", today=today, return_deadline=return_deadline, user="tama")


# このファイルが直接実行された場合にサーバーを起動
if __name__ == '__main__':
    # debug=Trueにすると、コードを変更したときに自動で再起動される
    app.run(debug=True)