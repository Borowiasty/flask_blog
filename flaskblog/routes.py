import secrets
import os
from PIL import Image
from flask import request, render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

posts = [
    {
        'author' : 'Corey Schafer',
        'title' : 'Blog post 1',
        'content' : 'First post contetnt',
        'date_posted': 'February 15, 2023'
    },
    {
        'author' : 'Jane doe',
        'title' : 'Blog post 2',
        'content' : 'Second post contetnt',
        'date_posted': 'February 16, 2023'
    }
]

# with app.app_context():
#      db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)

@app.route("/about")
def about():
    return render_template('about.html', title= 'about')

@app.route("/register", methods= ['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email= form.email.data, password= hashed_passwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title= 'register', form= form)

@app.route("/login", methods= ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page) 
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check email and password', 'danger')

    return render_template('login.html', title= 'Login', form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pictur_fn = random_hex + f_ext
    pictur_path = os.path.join(app.root_path, 'static/profile_pics', pictur_fn)
    
    output_size = (125, 125)
    resize_image = Image.open(form_picture)
    resize_image.thumbnail(output_size)
    resize_image.save(pictur_path)

    return pictur_fn

@app.route("/account",  methods= ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title= 'Account', image_file= image_file, form= form)