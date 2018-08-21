from flask import render_template, Blueprint, flash, redirect, url_for, session

from app.forms import LoginForm, RegistrationForm
from app.models.user import User
from app.routes.bbs import current_user
from app.utils import log

main = Blueprint('index', __name__)


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    return render_template('index.html', user=u)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User(username=form.data['username'], password=form.data['password'])
        if u.verify_username():
            flash("账号不存在")
            return redirect(url_for('.login'))
        elif u.validation_login():
            flash("密码错误")
            return redirect(url_for('.login'))
        session['username'] = u.username
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User.register(username=form.data['username'], password=form.data['password'], email=form.data['email'])
        if u is not None:
            session['username'] = u.username
            flash("注册成功", 'ok')
            return redirect(url_for('.index'))
    return render_template('register.html', form=form)


@main.route("/logout", methods=["GET"])
def logout():
    u = current_user()
    if u is not None:
        session.clear()
    return redirect(url_for('.index'))