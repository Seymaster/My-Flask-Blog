from flask import Blueprint,redirect,request,render_template,url_for,flash,abort
from flask_login import current_user,login_required
from syblogpost import db
from syblogpost.models import Comment,Blogpost
from syblogpost.comment.forms import CommentForm

comm = Blueprint('comm',__name__,url_prefix='/comm')


@comm.route('/comment', methods=['GET','POST'])
@login_required
def comment():
    form = CommentForm()
    # blogpost = Blogpost()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(body = form.body.data,
                              blogpost_id = 1)
            print(comment)
            db.session.add(comment)
            db.session.commit()
            flash('Comment created successful')
            return redirect(url_for('blog.blogspot'))
    return render_template('comment.html',form = form)