# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))  # 获得文件目录的绝对路径


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Python-flask]'
	FLASKY_MAIL_SENDER = 'Python Learner <cuijt1994@163.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '<269584357@qq.com>'
	FLASKY_POSTS_PER_PAGE = 10
	FLASKY_FOLLOWERS_PER_PAGE = 10

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/awakebird_dev'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/awakebird_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:632100@127.0.0.1:3306/awakebird'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}