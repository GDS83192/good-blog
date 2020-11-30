import os
import secrets
from datetime import datetime
from PIL import Image
from flask import Flask,render_template,url_for,flash,redirect,request,abort
from blogepedia import app,bcrypt,db
from blogepedia.forms import RegistrtionForm,Loginform,UpdateAccountInfo,NewPost
from blogepedia.model import Users,Post 
from flask_login import login_user,login_required,current_user,UserMixin,login_manager,logout_user




@app.route("/")
def home():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4,page=page)
	return render_template('index.html',posts=posts)



@app.route("/about")
def about():
    return render_template('about.html',title="About")



@app.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrtionForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Users(username = form.username.data , email = form.email.data , password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created. You are now able to login', 'success')
		return redirect(url_for('login'))
	return render_template('register.html',form=form,title="Register")



@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = Loginform()

	if form.validate_on_submit():
		user = Users.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get(url_for('account'))
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login Unsuccessful.Please check the email and the password.','danger')
		return redirect(url_for('login'))


	return render_template('login.html',form =form,title="Login")



@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))



# first we will be needing a funciton to save the pics uploaded
def save_picture(form_picture):
	img_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = img_hex+f_ext
	picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)

	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn


@login_required
@app.route("/account",methods=['GET','POST'])
def account():
	form = UpdateAccountInfo()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your profile has been successfully updated','success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file= url_for('static',filename ='profile_pics/'+current_user.image)
	return render_template('account.html',title="Account",image=image_file ,form=form)


# --------------------------------------------------------------------------------------------

def save_image(form_picture):
	img_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = img_hex+f_ext
	picture_path=os.path.join(app.root_path,'static/img/blog',picture_fn)

	output_size = (555,280)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn

@login_required
@app.route('/post/new',methods=['GET','POST'])
def new_post():
	form = NewPost()
	if form.validate_on_submit():
		if form.img_file.data:
			image = save_image(form.img_file.data)
			current_user.img_file = image
			post = Post(title = form.title.data,content=form.content.data,img_file=current_user.img_file,author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Your post has been created successsfully!','success')
			return redirect(url_for('home'))
		else:
			post = Post(title = form.title.data,content=form.content.data,author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Your post has been created successsfully!','success')
			return redirect(url_for('home'))		
	return render_template('new_post.html',title="New-Post",form=form)


@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html',title=post.title,post=post)


@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = NewPost()
	if form.validate_on_submit():
		if form.img_file.data:
			image = save_image(form.img_file.data)
			post.img_file = image
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been successfully updated','success')
		return redirect(url_for('post',post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('edit_post.html',title="Edit Post",post=post,form=form)


@app.route("/post/<int:post_id>/delete",methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!','success')
	return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = Users.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
	return render_template('user_post.html',title="User.username Posts",posts=posts,user=user)


# ----------------------------------------------------------------------------
@app.route("/contact")
def contact():
    return render_template('contact.html',title="Contact")

@app.route("/modal")
def modal():
    return render_template('modal_test.html',title="Modal")
    
    
if __name__ == "__main__":
    app.run()
