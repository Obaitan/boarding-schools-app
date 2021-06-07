from bse import db, login_manager
from datetime import datetime
from bse import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(admin_id):
    return Admin.get(int(admin_id))


# class Login(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), nullable=False, unique=True)
#     passwordHash = db.Column(db.String(60), nullable=False)

#     @property
#     def password(self):
#         return self.password()

#     @password.setter
#     def password(self, plain_text_password):
#         self.passwordHash = bcrypt.generate_password_hash(
#             plain_text_password).decode('utf-8')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    passwordHash = db.Column(db.String(60), nullable=False)

    @property
    def password(self):
        return self.password()

    @password.setter
    def password(self, plain_text_password):
        self.passwordHash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    excerpt = db.Column(db.String(300), nullable=False)
    article = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(40), nullable=False,
                       default='Unknown')
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)
    fp = db.Column(db.String(256), nullable=False)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'News {self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False,  unique=True)
    imageName = db.Column(db.Text, nullable=False)
    imagePath = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)

    def __repr__(self):
        return f'News {self.name}'


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colour1 = db.Column(db.String(7), nullable=False)
    colour2 = db.Column(db.String(7), nullable=False)
    name = db.Column(db.String(50), nullable=False,  unique=True)
    schoolType = db.Column(db.String(6), nullable=False)
    population = db.Column(db.String(75), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False,  unique=True)
    logo = db.Column(db.Text, nullable=False,  unique=True)
    logo_path = db.Column(db.String(256), nullable=False)
    pix = db.Column(db.Text, nullable=False,  unique=True)
    pixPath = db.Column(db.String(256), nullable=False)
    vidThumbnail = db.Column(db.Text, nullable=False)
    vidThumbnail_path = db.Column(db.String(256), nullable=False)
    facilities = db.Column(db.Text, nullable=True,  unique=True)
    academics = db.Column(db.Text, nullable=True,  unique=True)
    extra_curricular = db.Column(db.Text, nullable=True,  unique=True)
    pastoralCare = db.Column(db.Text, nullable=True,  unique=True)
    others1 = db.Column(db.Text, nullable=True,  unique=True)
    others2 = db.Column(db.Text, nullable=True,  unique=True)
    videoLink1 = db.Column(db.String(256), nullable=True, unique=True)
    videoLink2 = db.Column(db.String(256), nullable=True, unique=True)
    videoLink3 = db.Column(db.String(256), nullable=True, unique=True)
    videoLink4 = db.Column(db.String(256), nullable=True, unique=True)
    videoLink5 = db.Column(db.String(256), nullable=True, unique=True)
    feesForm = db.Column(db.Text, nullable=True,  unique=True)
    feesForm_path = db.Column(db.String(256), nullable=True)
    feesForm_link = db.Column(db.String(256), nullable=True, unique=True)
    appForm = db.Column(db.Text, nullable=True,  unique=True)
    appForm_path = db.Column(db.String(256), nullable=True)
    appForm_link = db.Column(db.String(256), nullable=True, unique=True)
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)
    country = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'News {self.name}'
