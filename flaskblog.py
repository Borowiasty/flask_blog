from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug= True)