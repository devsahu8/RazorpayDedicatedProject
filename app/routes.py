from flask import render_template,url_for,redirect,flash
from app.forms import IndexForm,LoginForm,RegisterForm,option3Form,option2Form
from app import app,db
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


@app.route("/option2",methods=["GET","POST"])
@login_required
def option2():
    orders=db.session.scalars(sa.select(Order).where(Order.reciptent_username==current_user.username)).all()
    total_amount=0
    for order in orders:
        total_amount+=order.amount
    if orders:
        flash(f"You have to pay a total of {total_amount} to {len(orders)} Producers.")
    else:
        flash("You have no pending orders to pay.")
    form=option2Form()
    if form.validate_on_submit():
        for order in orders:
            order.status="Paid"
        db.session.commit()
        flash("All order paid.")

        return redirect(url_for("option2"))
    return render_template("option2.html", orders=orders, total=total_amount,form=form)
    
    
@app.route("/option1")
@login_required
def option1():
    orders=db.session.scalars(sa.select(Order).where(Order.user==current_user)).all()
    if orders is None:
        flash("You have sended no orders.")
        return redirect(url_for("index"))
    return render_template("option1.html",orders=orders)

@app.route("/option3",methods=["GET","POST"])
@login_required
def option3():
    form=option3Form()
    if form.validate_on_submit():
        user=db.session.scalar(sa.select(User).where(User.username==form.senderName.data))
        if user is None:
            flash("This username does not exist in our database.")
            return redirect(url_for("option3"))
        new_order=Order(amount=form.reciptAmount.data,reciptent_username=user.username,user=current_user)
        db.session.add(new_order)
        db.session.commit()
        flash("A order has been created and sended to username.")
        return redirect(url_for("option3"))
    return render_template("option3.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        user=db.session.scalar(sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Username or password is wrong")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html",form=form,title="Sign-in")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

