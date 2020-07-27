from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = '5d6dd840fb92058ebb394c7b6bb10fcc9e97007a1b4f968e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1824840:aP9L2gEpDBh3DKb@csmysql.cs.cf.ac.uk:3306/c1824840'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
