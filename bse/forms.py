from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField, BooleanField, FileField, MultipleFileField, SelectField, RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, email_validator, ValidationError
from wtforms.fields.html5 import TelField, URLField, DateField
from bse.models import User

from wtforms.widgets import Input


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
    website = URLField("Website Address", validators=[DataRequired()])
    startDate = DateField("Commencement Date", validators=[DataRequired()])
    lnked = URLField("LinkedIn Page", validators=[DataRequired()])
    fb = URLField("Facebook Page", validators=[DataRequired()])
    twi = URLField("Twitter Page", validators=[DataRequired()])
    insta = URLField("Instagram Page", validators=[DataRequired()])
    skype = URLField("Skype Page", validators=[DataRequired()])
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
    submit = SubmitField("Submit Form")


class SubmitDocsForm(FlaskForm):
    name = TextField("Full Name", validators=[DataRequired()])
    school = TextField("Name of School Applied To",
                       validators=[DataRequired()])
    email = TextField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone Number", validators=[DataRequired()])
    docs = MultipleFileField("Documents", validators=[DataRequired()])
    submit = SubmitField("Send")


class BoardingSchoolsForm(FlaskForm):
    name = StringField("School Name", validators=[DataRequired()])
    col1 = StringField("Theme Colour 1", validators=[DataRequired()])
    col2 = StringField("Theme Colour 2", validators=[DataRequired()])
    schoolType = SelectField('School Type', [DataRequired()],
                             choices=[('', 'School Type'), ('girls', 'Girls Only'),
                                      ('boys', 'Boys Only'),
                                      ('co-educational', 'Co-Educational')])
    population = StringField("Student Population", validators=[DataRequired()])
    address = TextAreaField("School Address", validators=[DataRequired()])
    website = URLField("School Website", validators=[DataRequired()])
    country = SelectField('Country', [DataRequired()],
                          choices=[('', 'Choose A Country'), ('spain','Spain')])
    about = TextAreaField("School Introduction", validators=[DataRequired()])
    logo = FileField("School Logo", validators=[DataRequired()])
    badge = FileField("School Badge", validators=[DataRequired()])
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
    link1 = URLField("Link 1")
    link2 = URLField("Link 2")
    link3 = URLField("Link 3")
    link4 = URLField("Link 4")
    link5 = URLField("Link 5")
    submit = SubmitField("Submit Information")


class DocumentsForm(FlaskForm):
    name = SelectField("School Name", validators=[DataRequired()], choices=[
                       ('', 'Choose A Country'), ('spain', 'Spain')])
    forms = MultipleFileField("School Forms")
    feesLink = URLField("Link to Fees Form")
    appLink = URLField("Link to Application Form")
    submit = SubmitField("Submit Documents/Links")


class ImageForm(FlaskForm):
    name = SelectField("School Name", validators=[DataRequired()], choices=[
                       ('', 'Choose A Country'), ('spain', 'Spain')])
    schoolPix = MultipleFileField("School Forms", validators=[DataRequired()])
    vidPix = MultipleFileField("School Forms", validators=[DataRequired()])
    submit = SubmitField("Submit Pictures")
