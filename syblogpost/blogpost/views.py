from flask import Blueprint,redirect,request,render_template,url_for,flash,abort
from flask_login import current_user,login_required
from syblogpost import db
from syblogpost.models import Blogpost
from syblogpost.blogpost.forms import BlogpostForm

blog = Blueprint('blog',__name__,url_prefix='/blog')
# create
@blog.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogpostForm()
    if form.validate_on_submit():
        blog_post = Blogpost(title = form.title.data,
                            text   = form.text.data,
                            user_id = current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html',form = form )

# read blogpost
@blog.route('/<blog_post_id>')
def blog_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title = blog_post.title,
                            date =blog_post.date,post = blog_post
                            )

# # update
@blog.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    # using the backref "Author"
    if blog_post.author != current_user:
        abort(403)
    form = BlogpostForm()
    if form.validate_on_submit():
        # accessing the blogpost after query on line 35
        blog_post.title = form.title.data
        blog_post.text   = form.text.data
        db.session.commit()
        flash('Blog Post updated')
        return redirect(url_for('blog.blog_post',blog_post_id = blog_post_id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data  = blog_post.text
    return render_template('create_post.html', title = 'updating', form = form)
       
# delete
@blog.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403) 
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted')
    return redirect(url_for('core.index',blog_post_id = blog_post_id))
