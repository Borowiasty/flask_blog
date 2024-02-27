from flask import (Blueprint, render_template, url_for, flash,
                   redirect, abort, request)
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new",  methods= ['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post= Post(title= form.title.data, content= form.post_content.data, author= current_user)
        db.session.add(post)
        db.session.commit()

        flash("Post created", 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_post.html', title= 'New Post', form= form, legend= 'Update Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title= post.title, post= post)

@posts.route("/post/<int:post_id>/update",  methods= ['GET', 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.post_content.data
            db.session.commit()
            flash("Your post has been updated!", "success")
            return redirect(url_for('posts.post', post_id= post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.post_content.data = post.content
            return render_template('create_post.html', title= 'Update Post', form= form, legend= 'Update Post')


@posts.route("/post/<int:post_id>/delete",  methods= ['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))