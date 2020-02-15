from flask import Blueprint,render_template,request,redirect,url_for
from syblogpost.models import Blogpost

core = Blueprint('core', __name__,url_prefix='/core')

@core.route('/')
def index():
    page = request.args.get('page',1,type(int))
    blog_posts = Blogpost.query.order_by(Blogpost.date.desc()).paginate(page=page, per_page = 10)
    return render_template('index.html', blog_posts = blog_posts)

@core.route('/info')
def info():
    return render_template('info.html')