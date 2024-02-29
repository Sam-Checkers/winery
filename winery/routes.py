from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from winery.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from winery.models import User, Post, check_password_hash, db, contact_schema, contacts_schema
from flask_login import login_user, current_user, logout_user, login_required 
from winery import app
from winery.wine_list import red_1, red_2, red_3, red_4, red_5, red_6, red_7, white_1, white_2, white_3, white_4, lager_1, lager_2, lager_3, lager_4, lager_5

@app.route("/")
@app.route("/brewery")
def brewery():
    return render_template('brewery.html', title='brewery')

@app.route("/home")
def home():
    posts=Post.query.all()
    return render_template('home.html', posts=posts)

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

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/getdata')
def getdata():
    return {'test': '1'}

@app.route('/user_posts/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    user = User.query.get(user_id)
    if user:
        posts = user.posts
        serialized_posts = contacts_schema.dump(posts)
        return jsonify(serialized_posts)
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/user_posts/<int:user_id>/<int:post_id>', methods=['GET'])
def get_user_post(user_id, post_id):
    user = User.query.get(user_id)
    if user:
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        if post:
            serialized_post = contact_schema.dump(post)
            return jsonify(serialized_post)
        else:
            return jsonify({'message': 'Post not found for the user'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/user_posts/<int:user_id>/<int:post_id>', methods=['PUT'])
def update_user_post(user_id, post_id):
    user = User.query.get(user_id)
    if user:
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        if post:
            data = request.get_json()
            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            db.session.commit()
            return jsonify({'message': 'Post updated successfully'})
        else:
            return jsonify({'message': 'Post not found for the user'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/user_posts/<int:user_id>', methods=['POST'])
def create_user_post(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        new_post = Post(title=data.get('title'), content=data.get('content'), user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/user_posts/<int:user_id>/<int:post_id>', methods=['DELETE'])
def delete_user_post(user_id, post_id):
    user = User.query.get(user_id)
    if user:
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'message': 'Post deleted successfully'})
        else:
            return jsonify({'message': 'Post not found for the user'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404