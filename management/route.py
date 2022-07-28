from werkzeug.wrappers import Request
from management import app , db , encode
from datetime import date
import secrets
import os
from PIL import Image
from flask import render_template , url_for , flash , redirect , request
from management.form import *
from management.datbase import User , Post
from flask_login import login_user , current_user , logout_user , login_required


u='user'


@login_manager.user_loader
def load_user(user_id):
    if u =='user':
        return User.query.get(int(user_id))
    else :
        return Admin.query.get(int(user_id))



@app.route('/home')
@app.route('/')
def home():
    global u
    
    post = Post.query.all()
    user = User()
    return render_template('home.html' ,u=u, post = post , user = user)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= loginform()
    if form.validate_on_submit():
        global u

        if form.email.data[0:2]=='a:':
            u ='admin'
            admin = Admin.query.filter_by(email = form.email.data).first()

            if admin and encode.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                print(admin.admin)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful or you are Not admin , Please check the email and Password','danger')
        else:
            u='user'
            user = User.query.filter_by(email = form.email.data).first()
            if user and encode.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful , Please check the email and Password','danger')
    return render_template('login.html' , form=form)





@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = signupform()
    if form.validate_on_submit():
        encoded_pass = encode.generate_password_hash(form.password.data).decode('utf-8')
        print(form.username.data)
        user = User(username=form.username.data ,bio=form.bio.data,  email=form.email.data , password=encoded_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}','success')
        return redirect(url_for('login'))
    return render_template('signup.html' ,form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/pp' , picture_fn)
    outout_size = (300,300)
    i = Image.open(form_picture)
    i.thumbnail(outout_size)
    i.save(picture_path)
    return picture_fn




@app.route('/account' ,methods=['GET', 'POST'])
@login_required
def account():
    form = Accountform()
    if form.validate_on_submit():
        picture_file = save_picture(request.files['pic'])
        current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account is Updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static' , filename = 'pp/' + current_user.image_file)
    return render_template('account.html' ,  image_file = image_file , form = form)


@app.route('/newpost' ,methods=['GET', 'POST'])
@login_required
def newpost():
    form = postform()
    if form.validate_on_submit():
        post = Post(title=form.title.data , data=form.post_data.data , date_post=date.today() , uid=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(f'Post Created for {form.title.data}','success')
        return redirect(url_for('login'))
    return render_template('newpost.html' , form = form)

@app.route('/mypost' ,methods=['GET', 'POST'])
@login_required
def mypost():
    post = Post.query.filter_by(uid = current_user.id)
    return render_template('mypost.html' , post = post)


@app.route('/updatepost/<id>' , methods=[ 'GET', 'POST'] )
@login_required
def updatepost(id):
    form = postform()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.data = form.post_data.data
        db.session.commit()
        flash( 'Post is updated' , 'success' )
        return redirect(url_for('mypost'))
    form.title.data = post.title
    form.post_data.data = post.data 
    return render_template('newpost.html' ,  form = form , post = post)


@app.route('/deletepost/<id>' , methods=['GET', 'POST'] )
@login_required
def deletepost(id):
    db.session.delete(Post.query.get_or_404(id))
    db.session.commit()
    flash( 'Post is Deleted' , 'success' )
    return redirect(url_for('home'))

@app.route('/account/<id>' ,methods=['GET', 'POST'])
@login_required
def viewacc(id):
    user=User.query.get_or_404(id)
    post = Post.query.filter_by(uid = id).count()
    return render_template('viewacc.html',user=user ,post=post)



@app.route('/viewpost' ,methods=['GET', 'POST'] )
@login_required
def viewpost():
    global u
    post = Post.query.all()
    user = User()
    if request.method=='POST':
        ids=request.form.get('ID')
        po = Post.query.get_or_404(ids)      
        db.session.delete(po)
        db.session.commit()
        flash(f'The Post Deleted','success')
        return redirect(url_for('viewpost'))
    return render_template('viewpost.html' ,u=u, post = post , user = user)



@app.route('/viewaccs' ,methods=['GET', 'POST'])
@login_required
def viewaccs():
    global u
    user=User.query.all()
    if request.method=='POST':
        ids=request.form.get('ID')
        db.session.delete(User.query.get_or_404(ids))
        db.session.commit()
        flash(f'The User Deleted','success')
        return redirect(url_for('viewaccs'))
    return render_template('viewaccs.html',user=user,u=u)

@app.route('/readpost/<id>' ,methods=['GET', 'POST'])
def readpost(id):
    post = Post.query.filter_by(id=id)
    user = User.query.all()
    return render_template('readpost.html' , post = post,user=user)