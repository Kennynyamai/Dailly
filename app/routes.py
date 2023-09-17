from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(title=current_user.email, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_posts'))
    return render_template('main.html', form=form)

@app.route('/posts')
@login_required
def get_posts():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('posts.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main'))


    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/specific_post/<int:post_id>')
def specific_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('specific_post.html', post=post)



@app.route("/specific_post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('get_posts'))

