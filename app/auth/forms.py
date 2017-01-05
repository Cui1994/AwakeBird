# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(Form):
    email = StringField(u'邮箱地址', validators=[DataRequired(u'邮箱地址不能为空'), Length(1,64), Email(u'请输入正确的邮箱地址')])
    password = PasswordField(u'密码', validators=[DataRequired(u'密码不能为空')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
	email = StringField(u'邮箱地址', validators=[DataRequired(u'邮箱地址不能为空'), Length(1, 64), Email(u'请输入正确的邮箱地址')])
	username = StringField(u'用户名', validators=[DataRequired(u'用户名不能为空'), Length(1, 64)])
	password = PasswordField(u'密码', validators=[DataRequired(u'密码不能为空'), EqualTo('password2', message=u'两次输入的密码不一致')])
	password2 = PasswordField(u'确认密码', validators=[DataRequired(u'请确认密码')])
	submit = SubmitField(u'注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已经被注册了')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已经被使用')
