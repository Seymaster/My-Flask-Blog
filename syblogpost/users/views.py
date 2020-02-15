from flask import Blueprint,render_template,redirect,flash,request,url_for
from flask_login import login_user,current_user,logout_user,login_required
from syblogpost import db
from syblogpost.users.forms import Register,Login,updateform
from syblogpost.models import Users,Blogpost
from syblogpost.users.pics_handler import add_profile_pics

users = Blueprint('users',__name__,url_prefix='/users')

@users.route('/register',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        user = Users(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form = form)
    
# login
@users.route('/login', methods=['GET','POST'])
def login():
    #initializing the form created from the forms.py
    form = Login()
    if form.validate_on_submit():
    #querying the user from the database
        user = Users.query.filter_by(email = form.email.data).first()
    #checking password and confirming is user exist in the database
        if user.check_password(form.password.data) and user is not None:
    # function to carry out login imported from flask login
            login_user(user)
            # return "Log in Succesful"
    #to return user to any page he is before logging in  
            next = request.args.get('next')
    #if not return user to home page 
            if next == None or not next[0] == '/':
                next = url_for('core.index')
                return redirect(next)
    return render_template('login.html', form = form )

#logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#account info
@users.route('/account', methods=['POST','GET'])
@login_required
def account():
    form = updateform()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pics(form.picture.data,username)
            current_user.profile_image = pic 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated Successfully')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        profile_image = url_for('static',filename='profile_pics'+current_user.profile_image)
        return render_template('account.html',profile_image = profile_image,form = form)

@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = Users.query.filter_by(username = username).first()
    # _or_404()
    blog_posts = Blogpost.query.filter_by(author=user).order_by(Blogpost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_post.html',blog_posts = blog_posts, user=user)