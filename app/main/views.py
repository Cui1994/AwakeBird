# -*- coding:utf-8 -*-
from flask import render_template, sessions, redirect, url_for
from flask_login import login_required, current_user

from .forms import PostForm
from . import main
from .. import db
from ..models import  User, Post

@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    return render_template('user.html', username=username)

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    form.body.data = u'文章内容'
    return render_template('write.html', form=form)

