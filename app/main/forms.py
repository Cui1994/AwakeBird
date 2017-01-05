# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

from ..models import Post

class PostForm(Form):

    title = StringField(u'在这里输入文章标题', validators=[DataRequired(u'请输入标题'), Length(1, 200)])
    body = TextAreaField(u"写点什么吧...", validators=[DataRequired(u'内容不能为空')])
    submit = SubmitField(u'发布')

