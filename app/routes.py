from flask import render_template,url_for,redirect,flash
from app.forms import IndexForm,LoginForm
from app import app
from flask_login import current_user, login_user,logout_user,login_required
import sqlalchemy as sa
from app import db
from app.models import User,Order

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
@login_required
def index():
    form=IndexForm()
    if form.validate_on_submit():
        return redirect(url_for(form.choice.data))
    return render_template("index.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        user=db.session.scalar(sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(user.password_hash.data):
            flash("Username or password is wrong")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html",form=form,title="Sign-in")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))