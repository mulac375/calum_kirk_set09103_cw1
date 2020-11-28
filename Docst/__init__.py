from flask import Flask  # import flask functions
from flask_sqlalchemy import SQLAlchemy  # import sqlalchemy for database
from flask_bcrypt import Bcrypt # import bcrypt functions
from flask_login import LoginManager  # import login functions
from flask_mail import Message, Mail  # import email functions
mail = Mail() 

app = Flask(__name__) 
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # email configuration
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'calumkirkdesign@gmail.com'
app.config["MAIL_PASSWORD"] = ''

mail.init_app(app)

# upload configuration
app.config["IMAGE_UPLOADS"] = "/Users/calumkirk/desktop/docst/docst/static/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def allowed_image(filename):

    # only allows files with a . in the filename
    if not "." in filename:
        return False

    # Splits the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False
# secret key for database / login manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from docst import routes # imports from routes file in docst app
