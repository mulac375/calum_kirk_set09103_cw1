import os  # imports os
import secrets  # imports secrets
from PIL import Image  # imports image for account profile picture
from flask import render_template, url_for, flash, redirect, request, abort  # imports functions from flask
from docst import app, db, bcrypt  # imports database aspects
from docst.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ContactForm  # imports form functionality
from docst.models import User, Post  # imports user and post from models 
from flask_login import login_user, current_user, logout_user, login_required  # imports login information
from werkzeug.utils import secure_filename  # imports email functionality

@app.route("/")  # route for home
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/contact', methods=['GET', 'POST'])  # route for contact page and form
def contact():
  form = ContactForm()  # form function
 
  if request.method == 'POST':  # form functionality
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='calumkirkdesign@gmail.com', recipients=['calumkirkdesign@gmail.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True) # passes the template to the browser
 
  elif request.method == 'GET': # alternative to an else if statement which acts if the all above if statements are not utlised
    return render_template('contact.html', form=form)


    
@app.route("/upload", methods=['GET', 'POST']) # upload file route
def upload():
    
    if request.method == "POST": # if statement which requires post on request

        if request.files:
            
            if "filesize" in request.cookies:  # if statement which allows files up to maximum permitted size

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

            image = request.files["image"] #retrieves image
            
            if image.filename == "":
                print("Image must have filename") # alert to print if no filename
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension is not allowed") # alert if image not allowed
                return redirect(request.url)
            
            else:
                filename = secure_filename(image.filename) # uploads and saves file
            
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

                print("File Saved")

            return redirect(request.url)
    return render_template('upload.html', title='upload')



@app.route("/register", methods=['GET', 'POST']) # register route
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm() # register form function
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST']) # login route
def login():
    if current_user.is_authenticated: # user authentication if statement
        return redirect(url_for('home'))
    form = LoginForm() # login function
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # password verification
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout") # logout route
def logout():
    logout_user() # logout user function
    return redirect(url_for('home'))

def save_picture(form_picture): # save profile picture function
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) 

    output_size = (125, 125) # profile picture sizing
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 

 # account route
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()  # update account function
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # update profile picture
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():  # create post function
    form = PostForm()
    if form.validate_on_submit():  # validates and adds record to database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post) 
        db.session.commit()  # commits to database
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')  

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # post route and function
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):  # update post function
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
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])  # delete post function
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))