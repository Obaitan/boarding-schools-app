import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'bse/static/uploads')
# UPLOAD_FOLDER = os.path.join('bse', 'static/uploads')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '617444a610ba6230ead4e67a'

mail = Mail()
app.config["MAIL_SERVER"] = "mail.bravehost.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'webforms@boardingschoolsexperts.com'
app.config["MAIL_PASSWORD"] = 'Nosaevbu#486'

mail.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "admin"
login_manager.login_message_category = "info"



from bse import routes
