from flask import render_template,url_for,redirect
from app.forms import IndexForm,LoginForm
from app import app

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
def index():
    form=IndexForm()
    if form.validate_on_submit():
        return redirect(url_for(form.choice.data))
    return render_template("index.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html",form=form,title="Sign-in")
