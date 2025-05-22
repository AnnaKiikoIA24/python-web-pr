from flask import Flask 
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy 
#from flask_login import LoginManager 
#import os, config 
 
app = Flask(__name__) 
 
app.config.update( 
  DEBUG=True, 
  SECRET_KEY='strong secret key',
  # URL бази даних для MySQL з використанням драйвера PyMysql
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost/flask_app_schedule' 
)

#  Створюємо екземпляр об'єкта  SQLAlchemy, передавши йому екземпляр програми
db = SQLAlchemy(app) 
migrate = Migrate(app, db)

from . import views