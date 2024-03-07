from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from winery.forms import RegistrationForm, LoginForm, UpdateAccountForm
from winery.models import User, check_password_hash, db, contact_schema, contacts_schema, Wine, WineUser
from flask_login import login_user, current_user, logout_user, login_required 
from winery import app

@app.route("/")
@app.route("/brewery")
def brewery():
    wines = Wine.query.all()
    return render_template('brewery.html', title='brewery', wines=wines)

@app.route("/containers")
def containers():
    return render_template('containers.html', title='containers')

def wines():
    items = Wine.query.all()
    return render_template('home.html', items=items)

@app.route('/wines')
def display_wines():
    wines = Wine.query.all()
    return render_template('wines.html', wines=wines)

@app.route('/add_to_shelf', methods=['POST'])
def add_to_shelf():
    user_id = request.form['user_id']
    item_id = request.form['item_id']

    user = User.query.get(user_id)
    item = Wine.query.get(item_id)
    user.shelf.append(item)
    db.session.commit()

@app.route('/shelf/<int:user_id>')
def shelf(user_id):
    user = User.query.get(user_id)
    shelf_items = user.shelf
    return render_template('home.html', user=user, shelf_items=shelf_items)

@app.route('/remove_from_shelf', methods=['POST'])
def remove_from_cart():
    user_id = request.form['user_id']
    item_id = request.form['item_id']

    user = User.query.get(user_id)
    item = Wine.query.get(item_id)
    user.cart.remove(item)
    db.session.commit()
    
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first.data
        last_name = form.last.data
        email = form.email.data
        password = form.password.data
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user = User(first_name, last_name, username, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email,password)
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('Success')
            return redirect(url_for('home'))
        else:
            flash('Check email and password')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)