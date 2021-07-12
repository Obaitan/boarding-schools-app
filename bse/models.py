from bse import db, login_manager
from datetime import datetime
from bse import bcrypt
from flask_login import UserMixin


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'News': News, 'Country': Country, 'Schools': Schools, 'Imgaes': Images, 'Thumbnails': Thumbnails, 'Documents', Documents}


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    firstName = db.Column(db.String(30), nullable=False, unique=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    excerpt = db.Column(db.String(300), nullable=False, unique=True)
    article = db.Column(db.Text, nullable=False, unique=True)
    author = db.Column(db.String(40), nullable=False,
                       default='Unknown')
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)
    imagePath = db.Column(db.String(256), nullable=False)
    image = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f'News {self.id}'


class Country(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False,  unique=True)
    flag = db.Column(db.Text, nullable=False, unique=True)
    flagPath = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Country: {self.name}'


class Schools(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    colour1 = db.Column(db.String(7), nullable=False)
    colour2 = db.Column(db.String(7), nullable=False)
    schoolName = db.Column(db.String(100), nullable=False, unique=True)
    schoolType = db.Column(db.String(6), nullable=False)
    population = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(60), nullable=False)
    about = db.Column(db.Text, nullable=False)
    logo = db.Column(db.Text, nullable=False, unique=True)
    logoPath = db.Column(db.String(256), nullable=False)
    badge = db.Column(db.Text, nullable=False, unique=True)
    badgePath = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)
    country = db.Column(db.String(35), nullable=False)
    facilities = db.Column(db.Text, nullable=True)
    academics = db.Column(db.Text, nullable=True)
    extra = db.Column(db.Text, nullable=True)
    care = db.Column(db.Text, nullable=True)
    newHeading = db.Column(db.Text, nullable=True)
    newBody = db.Column(db.Text, nullable=True)
    newHeading2 = db.Column(db.Text, nullable=True)
    newBody2 = db.Column(db.Text, nullable=True)
    newHeading3 = db.Column(db.Text, nullable=True)
    newBody3 = db.Column(db.Text, nullable=True)
    link1 = db.Column(db.String(256), nullable=True)
    link2 = db.Column(db.String(256), nullable=True)
    link3 = db.Column(db.String(256), nullable=True)
    link4 = db.Column(db.String(256), nullable=True)
    link5 = db.Column(db.String(256), nullable=True)
    tour = db.Column(db.String(256), nullable=True)
    appLink = db.Column(db.String(256), nullable=True)
    feesLink = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'School: {self.schoolName}'


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schoolName = db.Column(db.Text, nullable=False)
    schoolPix = db.Column(db.Text, nullable=False)
    schoolPixPath = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'Image {self.id}'


class Thumbnails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    vidPix = db.Column(db.Text, nullable=False)
    vidPixPath = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'Thumbnail {self.id}'


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schoolName = db.Column(db.Text, nullable=False)
    appForm = db.Column(db.Text, nullable=True, unique=True)
    appFormsPath = db.Column(db.String(256), nullable=True)
    feesForm = db.Column(db.Text, nullable=True, unique=True)
    feesFormsPath = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'Form: {self.name}'
