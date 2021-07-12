from collections import Iterable
from werkzeug.datastructures import FileStorage
from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField, BooleanField, FileField, MultipleFileField, SelectField, RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, email_validator, ValidationError, StopValidation, InputRequired, URL, Optional
from wtforms.fields.html5 import TelField, URLField, DateField
from bse.models import News, User, Country, Schools, Images, Thumbnails, Documents
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from werkzeug.utils import secure_filename

from wtforms.widgets import Input


class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):

        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if any(filename.endswith('.' + x) for x in self.upload_set):
                    return

                raise StopValidation(self.message or field.gettext(
                    'File does not have the approved extension: {extensions}'
                ).format(extensions=', '.join(self.upload_set)))

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(self.message or field.gettext(
                    'File does not have the approved extension.'
                ))


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    name = TextField("Name", validators=[DataRequired(), Length(min=3)])
    email = TextField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[
                            DataRequired(), Length(min=50)])
    phone = TelField("Phone Number", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")


class SchoolsForm(FlaskForm):
    schoolName = TextField("School Name", validators=[
                           DataRequired(), Length(min=12)])
    title = TextField("Contact's Title", validators=[DataRequired()])
    contactName = TextField("Contact's Full Name", validators=[
        DataRequired(), Length(min=5)])
    email = TextField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone Number", validators=[DataRequired()])
    comments = TextAreaField("Additional Comments")
    checkbox = BooleanField(
        'I declare that the information contained in this application and all supporting doumentation is true and correct.', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit form")


class AgentsForm(FlaskForm):
    companyName = TextField("Company Name", validators=[DataRequired()])
    companyAddress = TextField("Company Address", validators=[DataRequired()])
    city = TextField("City", validators=[DataRequired()])
    state = TextField("State", validators=[DataRequired()])
    countryName = TextField("Country", validators=[DataRequired()])
    email = TextField("Email", validators=[DataRequired(), Email()])
    phone1 = TelField("Phone Number 1", validators=[DataRequired()])
    phone2 = TelField("Phone Number 2", validators=[DataRequired()])
    whatsApp = TelField("WhatsApp Number", validators=[DataRequired()])
    website = URLField("Website Address", validators=[DataRequired(), URL()])
    startDate = DateField("Commencement Date", validators=[DataRequired()])
    lnked = URLField("LinkedIn Page", validators=[DataRequired(), URL()])
    fb = URLField("Facebook Page", validators=[Optional(), URL()])
    twi = URLField("Twitter Page", validators=[Optional(), URL()])
    insta = URLField("Instagram Page", validators=[Optional(), URL()])
    skype = URLField("Skype Page", validators=[Optional(), URL()])
    # Second Part
    service1 = TextField("Service 1", validators=[DataRequired()])
    service2 = TextField("Service 2")
    service3 = TextField("Service 4")
    service4 = TextField("Service 4")
    country1 = TextField("Country 1", validators=[DataRequired()])
    country2 = TextField("Country 2")
    country3 = TextField("Country 3")
    country4 = TextField("Country 4")
    group1 = TextField("Groupy 1", validators=[DataRequired()])
    group2 = TextField("Group 2")
    group3 = TextField("Group 3")
    group4 = TextField("Group 4")
    refInstitution = TextField(
        "Name of Institution", validators=[DataRequired()])
    refName = TextField("Name of Person", validators=[DataRequired()])
    refPhone = TelField("Phone Number", validators=[DataRequired()])
    refEmail = TextField("Email Address", validators=[DataRequired(), Email()])
    refInstitution2 = TextField(
        "Name of Institution", validators=[DataRequired()])
    refName2 = TextField("Name of Person", validators=[DataRequired()])
    refPhone2 = TelField("Phone Number", validators=[DataRequired()])
    refEmail2 = TextField("Email Address", validators=[
                          DataRequired(), Email()])
    checkbox = BooleanField(
        'I declare that the information contained in this application and all supporting doumentation is true and correct.', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit Form")


class SubmitDocsForm(FlaskForm):
    name = TextField("Full Name", validators=[DataRequired()])
    school = TextField("Name of School Applied To",
                       validators=[DataRequired()])
    email = TextField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone Number", validators=[DataRequired()])
    docs = MultipleFileField("Documents", validators=[
                             DataRequired(), MultiFileAllowed(['pdf'])])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit Documents")


class BoardingSchoolsForm(FlaskForm):
    def query_factory():
        return [r.name for r in Country.query.all()]

    def get_pk(obj):
        return obj

    def validate_schoolName(self, schoolName_to_check):
        school = Schools.query.filter_by(
            schoolName=schoolName_to_check.data).first()
        if school:
            raise ValidationError(
                'School Already Exists! Please Add A Different School.')

    def validate_logo(self, logo_to_check):
        logo_to_check = secure_filename(logo_to_check.data.filename)
        logo = Schools.query.filter_by(logo=logo_to_check).first()
        if logo:
            raise ValidationError(
                'Image Already Used! Please Use The Right School Logo.')

    def validate_badge(self, badge_to_check):
        badge_to_check = secure_filename(badge_to_check.data.filename)
        badge = Schools.query.filter_by(badge=badge_to_check).first()
        if badge:
            raise ValidationError(
                'Image Already Used! Please Use The Right School Badge.')

    schoolName = StringField("School Name", validators=[DataRequired()])
    col1 = StringField("Theme Colour 1", validators=[DataRequired()])
    col2 = StringField("Theme Colour 2", validators=[DataRequired()])
    schoolType = SelectField('School Type', [DataRequired()],
                             choices=[('', 'School Type'), ('girls', 'Girls Only'),
                                      ('boys', 'Boys Only'),
                                      ('co-educational', 'Co-Educational')])
    population = StringField("Student Population", validators=[DataRequired()])
    address = TextAreaField("School Address", validators=[DataRequired()])
    website = URLField("School Website", validators=[DataRequired(), URL()])
    country = QuerySelectField(label=u'Select Country', validators=[
        DataRequired()], query_factory=query_factory, get_pk=get_pk)
    about = TextAreaField("School Introduction", validators=[DataRequired()])
    logo = FileField("School Logo", validators=[
                     DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    badge = FileField("School Badge", validators=[
                      DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    facilities = TextAreaField("Boarding Facilities")
    academics = TextAreaField("Academic Programmes")
    extra = TextAreaField("Extra-Curricular Activities")
    care = TextAreaField("Pastoral Care")
    newHeading = TextField("New Heading")
    newBody = TextAreaField("New Body")
    newHeading2 = TextField("New Heading 2")
    newBody2 = TextAreaField("New Body 2")
    newHeading3 = TextField("New Heading 3")
    newBody3 = TextAreaField("New Body 3")
    link1 = URLField("Link 1", validators=[Optional(), URL()])
    link2 = URLField("Link 2", validators=[Optional(), URL()])
    link3 = URLField("Link 3", validators=[Optional(), URL()])
    link4 = URLField("Link 4", validators=[Optional(), URL()])
    link5 = URLField("Link 5", validators=[Optional(), URL()])
    tour = URLField("Virtual Tour Link", validators=[Optional(), URL()])
    feesLink = URLField("Link to Fees Form", validators=[Optional(), URL()])
    appLink = URLField("Link to Application Form",
                       validators=[Optional(), URL()])
    submit = SubmitField("Submit Information")


class ImageForm(FlaskForm):
    def query_factory():
        return [s.schoolName for s in Schools.query.all()]

    def get_pk(obj):
        return obj

    schoolName = QuerySelectField(label=u'School Name', validators=[
        DataRequired()], query_factory=query_factory, get_pk=get_pk)
    schoolPix = MultipleFileField("School Forms", validators=[
                                  DataRequired(), MultiFileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Submit Pictures")


class ThumbnailForm(FlaskForm):
    def query_factory():
        return [s.schoolName for s in Schools.query.all()]

    def get_pk(obj):
        return obj

    name = QuerySelectField(label=u'School Name', validators=[
        DataRequired()], query_factory=query_factory, get_pk=get_pk)
    vidPix = MultipleFileField("School Forms", validators=[
                               DataRequired(), MultiFileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Submit Images")


class DocumentsForm(FlaskForm):
    def query_factory():
        return [s.schoolName for s in Schools.query.all()]

    def get_pk(obj):
        return obj

    def validate_appForm(self, appForm_to_check):
        appForm_to_check = secure_filename(appForm_to_check.data.filename)
        form1 = Documents.query.filter_by(appForm=appForm_to_check).first()
        if form1:
            raise ValidationError(
                'Document Already Uploaded! Please Select The Right School Form.')

    def validate_feesForm(self, feesForm_to_check):
        feesForm_to_check = secure_filename(feesForm_to_check.data.filename)
        form2 = Documents.query.filter_by(feesForm=feesForm_to_check).first()
        if form2:
            raise ValidationError(
                'Document Already Uploaded! Please Select The Right School Form.')

    schoolName = QuerySelectField(label=u'School Name', validators=[
        DataRequired()], query_factory=query_factory, get_pk=get_pk)
    appForm = FileField("School Application Form", validators=[
                        Optional(), FileAllowed(['pdf'])])
    feesForm = FileField("School Fees Form", validators=[
                         Optional(), FileAllowed(['pdf'])])
    submit = SubmitField("Submit Documents")


class NewsForm(FlaskForm):
    def validate_title(self, title_to_check):
        ti = News.query.filter_by(
            title=title_to_check.data).first()
        if ti:
            raise ValidationError(
                'Article Title Already Exists! Please Use A Different Title.')

    def validate_excerpt(self, excerpt_to_check):
        ex = News.query.filter_by(
            excerpt=excerpt_to_check.data).first()
        if ex:
            raise ValidationError(
                'Article Excerpt Already Exists! Please Enter A Different Excerpt.')
    
    def validate_article(self, article_to_check):
        art = News.query.filter_by(
            article=article_to_check.data).first()
        if art:
            raise ValidationError(
                'Article Already Exists! Please Enter A Different Article.')

    def validate_image(self, image_to_check):
        image_to_check = secure_filename(image_to_check.data.filename)
        ig = News.query.filter_by(image=image_to_check).first()
        if ig:
            raise ValidationError(
                'Image Already Used! Please Use A Different Image.')
    
    title = StringField('Article Title', validators=[DataRequired()])
    excerpt = TextAreaField("Article Excerpt", validators=[DataRequired(), Length(max=350)])
    article = TextAreaField("Article", validators=[DataRequired()])
    author = StringField('Author Name', validators=[DataRequired()])
    image = FileField("School Address", validators=[DataRequired()])
    submit = SubmitField('Publish Article')
