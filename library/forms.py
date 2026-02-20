from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        "ユーザーID", validators=[DataRequired(), Length(min=2, max=80)]
    )
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")
    class Meta:
        csrf = False


class BookRequestForm(FlaskForm):
    title = StringField("書名", validators=[DataRequired()])
    author = StringField("著者", validators=[DataRequired()])
    reason = TextAreaField("リクエスト理由", validators=[DataRequired()])
    submit = SubmitField("申請する")


class SearchForm(FlaskForm):
    keyword = StringField(
        "タイトルまたは著者",
        validators=[DataRequired()],
        render_kw={"placeholder": "キーワードを入力"},
    )
    submit = SubmitField("検索")


class SignupForm(FlaskForm):
    username = StringField(
        "希望ユーザID（半角英数字）",
        validators=[DataRequired(), Length(min=2, max=80), Regexp(r"^[a-z0-9A-Z]+$", message="半角英数字のみ使用してください")],
    )
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("サインアップ")
    class Meta:
        csrf = False
