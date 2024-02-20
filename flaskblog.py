from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration_form, Login_form

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c9755297e7db0233629e850cfba2446e'

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)

@app.route("/about")
def about():
    return render_template('about.html', title= 'about')

@app.route("/register", methods= ['GET', 'POST'])
def register():
    form = Registration_form()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', title= 'register', form= form)

@app.route("/login", methods= ['GET', 'POST'])
def login():
    form = Login_form()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have benn logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check username and password', 'danger')

    return render_template('login.html', title= 'Login', form= form)


if __name__ == '__main__':
    app.run(debug= True)