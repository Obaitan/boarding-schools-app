import os

from bse import app, db, bcrypt, mail
from flask import render_template, url_for, redirect, request, flash, send_from_directory, session
from bse.models import News, User, Country, Schools, Images, Thumbnails, Documents
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from bse.forms import LoginForm, ContactForm, SchoolsForm, AgentsForm, SubmitDocsForm, BoardingSchoolsForm, ImageForm, ThumbnailForm, DocumentsForm, NewsForm, EditNewsForm, ApplyForm, EditSchoolForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from sqlalchemy import exc

from datetime import timedelta


ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg'])


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


@app.route('/static/uploads/<filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
@app.route('/home')
def home():
    news = News.query.order_by(News.id.desc()).all()
    return render_template('pages/index.html', news=news)


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/services')
def services():
    return render_template('pages/services.html')


@app.route('/schools')
def schools():
    # schools = Schools.query.filter_by(country=country).all()
    countries = Country.query.order_by(Country.id).all()
    return render_template('pages/schools.html', countries=countries)


@app.route('/schools/<string:name>')
def schools_by_country(name):
    schools = Schools.query.filter_by(country=name).all()
    return render_template('pages/show-schools.html', schools=schools)


@app.route('/schools/<string:name>/<string:name2>')
def single_school(name, name2):
    college = Schools.query.filter_by(schoolName=name2).first()
    images = Images.query.filter_by(schoolName=name2).all()
    thumbs = Thumbnails.query.filter_by(name=name2).all()
    docs = Documents.query.filter_by(schoolName=name2).first()
    return render_template('pages/school-template-one.html', college=college, images=images, thumbs=thumbs, docs=docs)


@app.route('/schools/apply/<string:name>', methods=['GET', 'POST'])
def apply_form(name):
    form = ApplyForm()
    school = Schools.query.filter_by(schoolName=name).first()
    url = school.appLink
    if request.method == 'POST':
        if form.validate() == False:
            flash(
                'Please meet the requirement for each field and click "CONTINUE APPLICATION".', category='danger')
            return render_template('pages/apply-form.html', form=form, school=school)
        else:
            subject = "New Message From School Applicant Form"
            msg = Message(subject, sender='webforms@boardingschoolsexperts.com',
                          recipients=['admissions@boardingschoolsexperts.com'])

            form.school.data = school.schoolName

            msg.html = f"<p><b>STUDENT'S DETAILS</b><br><b>First Name</b>: {form.fName.data}<br><b>Surname</b>: {form.sName.data}<br><b>Date of Birth</b>: {form.birthDate.data}<br><b>Present School</b>: {form.p_school.data}<br><b>School Applying To</b>: {form.school.data}<br><b>Home Address</b>: {form.home_address.data}<br><br><b>GUARDIAN'S DETAILS<br><b>Full Name</b>: {form.full_name.data}<br><b>Email</b>: {form.email.data}<br><b>Phone Number</b>: {form.phone.data}<br><b>Address</b>: {form.address.data}</p>"

            mail.send(msg)
            return redirect(url)

    elif request.method == 'GET':
        return render_template('pages/apply-form.html', form=form, school=school)


@app.route('/schools/partnership_form', methods=['GET', 'POST'])
def schools_form():
    form = SchoolsForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash(
                'Please meet the requirement for each field and click "SUBMIT FORM" again.', category='danger')
            return render_template('pages/schools-form.html', form=form)
        else:
            subject = "New Message From Schools Parnership Form"
            msg = Message(subject, sender='webforms@boardingschoolsexperts.com',
                          recipients=['info@boardingschoolsexperts.com'])

            msg.html = f'<p><b>From</b>: {form.title.data} {form.contactName.data}<br><b>School Name</b>: {form.schoolName.data}<br><b>Email</b>: {form.email.data}<br><b>Phone Number</b>: {form.phone.data}<br><br>{form.comments.data}</p>'

            mail.send(msg)

            flash('Your form has been submited! We will be in touch with you shortly',
                  category='success')
            return redirect(url_for('schools_form'))

    elif request.method == 'GET':
        return render_template('pages/schools-form.html', form=form)


@app.route('/agents')
def agents():
    return render_template('pages/agents.html')


@app.route('/agents/partnership_form', methods=['GET', 'POST'])
def agents_form():
    form = AgentsForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash(
                'Please provide valid information for all required fields before clicking "SUBMIT FORM" again.', category='danger')
            return render_template('pages/agents-form.html', form=form)
        else:
            subject = "New Message From Agents Parnership Form"
            msg = Message(subject, sender='webforms@boardingschoolsexperts.com',
                          recipients=['info@boardingschoolsexperts.com'])

            msg.html = f'<p><b>COMPANY INFORMATION..........</b><br><b>Company Name</b>: {form.companyName.data}<br><b>Company Address</b>: {form.companyAddress.data}<br><b>City</b>: {form.city.data}<br><b>State</b>: {form.state.data}<br><b>Country</b>: {form.countryName.data}<br><b>Email Address</b>: {form.email.data}<br><b>Phone 1</b>: {form.phone1.data}<br><b>Phone 2</b>: {form.phone2.data}<br><b>WhatsApp</b>: {form.whatsApp.data}<br><b>Company Website</b>: {form.website.data}<br><b>Operations Commencement Date</b>: {form.startDate.data}<br><b>LinkedIn Page</b>: {form.lnked.data}<br><b>Facebook Page</b>: {form.fb.data}<br><b>Twitter Page</b>: {form.twi.data}<br><b>Instagram Page</b>: {form.insta.data}<br><b>skype</b>: {form.skype.data}<br><br><b>RECRUITMENT DETAILS..........</b><br><b>Services We Provide</b><br><b>A</b>: {form.service1.data}<br><b>B</b>: {form.service2.data}<br><b>C</b>: {form.service3.data}<br><b>D</b>: {form.service4.data}<br><br><b>Countries We Work In</b><br><b>A</b>: {form.country1.data}<br><b>B</b>: {form.country2.data}<br><b>C</b>: {form.country3.data}<br><b>D</b>: {form.country4.data}<br><br><b>Associations/Groups We Belong To<br><b>A</b>: {form.group1.data}<br><b>B</b>: {form.group2.data}<br><b>C</b>: {form.group3.data}<br><b>D</b>: {form.group4.data}<br><br><b>Reference 1</b><br><b>Name of Institution</b>: {form.refInstitution.data}<br><b>Name of Person</b>: {form.refName.data}<br><b>Phone Number</b>: {form.refPhone.data}<br><b>Email</b>: {form.refEmail.data}<br><br><b>Reference 2</b><br><b>Name of Institution</b>: {form.refInstitution2.data}<br><b>Name of Person</b>: {form.refName2.data}<br><b>Phone Number</b>: {form.refPhone2.data}<br><b>Email</b>: {form.refEmail2.data}</p>'

            mail.send(msg)

            flash('Your form has been submited! We will be in touch with you shortly',
                  category='success')
            return redirect(url_for('agents_form'))

    else:
        return render_template('pages/agents-form.html', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash(
                'Please meet the requirement for each field and click "SEND" again.', category='danger')
            return render_template('pages/contact.html', form=form)
        else:
            subject = "New Message From Contact Form"
            msg = Message(subject, sender='webforms@boardingschoolsexperts.com',
                          recipients=['info@boardingschoolsexperts.com'])

            msg.html = f'<p><b>From</b>: {form.name.data}<br><b>Email</b>: {form.email.data}<br><b>Phone Number</b>: {form.phone.data}<br><br>{form.message.data}</p>'

            mail.send(msg)

            return render_template('pages/contact.html', form=form, success=True)

    elif request.method == 'GET':
        return render_template('pages/contact.html', form=form)


@app.route('/submit_docs', methods=['GET', 'POST'])
def submit_docs():
    form = SubmitDocsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            subject = "New Message From Applicant On Website."
            msg = Message(subject, sender='webforms@boardingschoolsexperts.com',
                          recipients=['admissions@boardingschoolsexperts.com'])
            msg.html = f'<p><b>From</b>: {form.name.data}<br><b>School Applied To</b>: {form.school.data}<br><b>Email</b>: {form.email.data}<br><b>Phone Number</b>: {form.phone.data}</p>'

            for data in form.docs.data:
                msg.attach(secure_filename(data.filename),
                           "application/octect-stream", data.read())
            mail.send(msg)
            flash(
                'Your Message Has Been Sent! We Will Be In Touch With You Shortly.', category='success')
            return redirect(request.url)
        else:
            flash(
                f'Please Meet The Requirements of The Form Fields And Submit Again.', category='danger')
            return render_template('pages/submit-docs-form.html', form=form)
    else:
        return render_template('pages/submit-docs-form.html', form=form)


@app.route('/news')
def news():
    news = News.query.order_by(News.id.desc()).all()
    return render_template('news/news-page.html', news=news)


@app.route('/news/single/<int:id>')
def news_single(id):
    news = News.query.get_or_404(id)
    last_few = News.query.order_by(News.id.desc()).limit(3)
    return render_template('news/single-article.html', news=news, last=last_few)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin')
                return redirect(next_page)
        else:
            flash(f'Incorrect Username Or Password! Please Try Again.',
                  category='danger')
            return redirect(request.url)
    return render_template('admin/admin-login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('admin'))


@app.route('/admin/dashboard')
@login_required
def dashboard():
    return render_template('admin/admin-dashboard.html')


@app.route('/admin/news')
@login_required
def dashboard_news():
    news = News.query.order_by(News.id.desc()).all()
    return render_template('admin/articles.html', news=news)


@app.route('/admin/news/articles/add', methods=['GET', 'POST'])
@login_required
def new_article():
    form = NewsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            excerpt = form.excerpt.data
            article = form.article.data
            image = form.image.data

            if image:
                imageName = secure_filename(image.filename)

                new_post = News(
                    title=title, excerpt=excerpt, article=article, author=author, image=imageName, imagePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], imageName)))
                db.session.add(new_post)
                db.session.commit()
                image.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], imageName))
                flash(f'News Article Published Successfully!.',
                      category='success')
                return redirect(request.url)
            else:
                flash(f'No Image Attached', category='danger')
                return render_template('admin/add-article.html', form=form)
        else:
            flash(
                f'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
            return render_template('admin/add-article.html', form=form)
    else:
        return render_template('admin/add-article.html', form=form)


@ app.route('/admin/news/articles/delete/<int:id>')
@login_required
def delete_article(id):
    entry = News.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    filepath = entry.imagePath
    os.remove(filepath)
    return redirect('/admin/news')


@ app.route('/admin/news/articles/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_article(id):
    news = News.query.get_or_404(id)
    form = EditNewsForm(obj=news)
    if request.method == "POST":
        if form.validate_on_submit():
            news.title = form.title.data
            news.author = form.author.data
            news.excerpt = form.excerpt.data
            news.article = form.article.data
            db.session.commit()
            return redirect(url_for('dashboard_news'))
        else:
            return render_template('admin/edit-article.html', news=news, form=form)
    else:
        return render_template('admin/edit-article.html', news=news, form=form)


@app.route('/admin/schools')
@login_required
def admin_schools():
    schools = Schools.query.order_by(Schools.id).all()
    return render_template('admin/admin-schools.html', schools=schools)


@app.route('/admin/schools/new/information', methods=['GET', 'POST'])
@login_required
def new_school_info():
    form = BoardingSchoolsForm()
    s = Schools.query.filter_by(schoolName=form.schoolName.data).first()
    if s:
        flash(f'{form.schoolName.data} Already Has An Entry! Go To Schools Table To Edit It.', category='danger')
        return redirect(request.url)
    else:
        if request.method == "POST":
            if form.validate_on_submit():
                schoolName = form.schoolName.data
                country = form.country.data
                col1 = form.col1.data
                col2 = form.col2.data
                schType = form.schoolType.data
                population = form.population.data
                website = form.website.data
                address = form.address.data
                about = form.about.data
                facilities = form.facilities.data
                academics = form.academics.data
                extra = form.extra.data
                care = form.care.data
                nH = form.newHeading.data
                nB = form.newBody.data
                nH2 = form.newHeading2.data
                nB2 = form.newBody2.data
                nH3 = form.newHeading3.data
                nB3 = form.newBody3.data
                link1 = form.link1.data
                link2 = form.link2.data
                link3 = form.link3.data
                link4 = form.link4.data
                link5 = form.link5.data
                tour = form.tour.data
                appLink = form.appLink.data
                feesLink = form.feesLink.data
                logo = form.logo.data
                badge = form.badge.data

                if logo and badge:
                    logoName = secure_filename(logo.filename)
                    badgeName = secure_filename(badge.filename)

                    new_school = Schools(
                        colour1=col1, colour2=col2, schoolName=schoolName, schoolType=schType, population=population, address=address, website=website, about=about, country=country, logo=logoName, logoPath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], logoName)), badge=badgeName, badgePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], badgeName)), facilities=facilities, academics=academics, extra=extra, care=care, newHeading=nH, newBody=nB, newHeading2=nH2, newBody2=nB2, newHeading3=nH3, newBody3=nB3, link1=link1, link2=link2, link3=link3, link4=link4, link5=link5, tour=tour, appLink=appLink, feesLink=feesLink)

                    db.session.add(new_school)
                    db.session.commit()
                    logo.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], logoName))
                    badge.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], badgeName))
                    flash(f'Information for {schoolName} Has Been Saved. Please Upload Images And Forms Next.',
                          category='success')
                    return redirect(request.url)
                else:
                    flash(
                        'Please Upload Images (PNG / JEPG / JPG) For Both Of The Image Fields', category='danger')
                    return render_template('admin/add-school-information.html', form=form)
            else:
                flash(
                    f'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
                return render_template('admin/add-school-information.html', form=form)
        else:
            return render_template('admin/add-school-information.html', form=form)


@app.route('/admin/schools/new/images', methods=['GET', 'POST'])
@login_required
def new_school_images():
    form = ImageForm()
    i = Images.query.filter_by(schoolName=form.schoolName.data).first()
    if i:
        flash(f'{form.schoolName.data} Already Has An Entry. Go To Schools Table To Edit It.', category='danger')
        return redirect(request.url)
    else:
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.schoolName.data
                for pix in form.schoolPix.data:
                    schPixName = secure_filename(pix.filename)
                    schImage = Images(schoolName=name, schoolPix=schPixName, schoolPixPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], schPixName)))
                    db.session.add(schImage)
                    pix.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], schPixName))
                db.session.commit()
                flash(
                    f'Images For {name} Have Been Uploaded Successfully.', category='success')
                return redirect(request.url)
            else:
                flash(
                    f'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
                return render_template('admin/add-school-images.html', form=form)
        else:
            return render_template('admin/add-school-images.html', form=form)


@app.route('/admin/schools/new/thumbnails', methods=['GET', 'POST'])
@login_required
def new_school_thumbnails():
    form = ThumbnailForm()
    t = Thumbnails.query.filter_by(name=form.name.data).first()
    if t:
        flash(
            f'{form.name.data} Already Has An Entry! Click On Its Badge To Edit It.', category='danger')
        return redirect(request.url)
    else:
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.name.data
                for image in form.vidPix.data:
                    vidPixName = secure_filename(image.filename)
                    vidImage = Thumbnails(name=name, vidPix=vidPixName, vidPixPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], vidPixName)))
                    db.session.add(vidImage)
                    image.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], vidPixName))
                db.session.commit()
                flash(
                    f'YouTube Images For {name} Have Been Uploaded Successfully.', category='success')
                return redirect(request.url)
            else:
                flash(
                    f'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
                return render_template('admin/add-school-thumbnails.html', form=form)
        else:
            return render_template('admin/add-school-thumbnails.html', form=form)


@app.route('/admin/schools/new/forms', methods=['GET', 'POST'])
@login_required
def new_school_forms():
    form = DocumentsForm()
    school_name = Documents.query.filter_by(
        schoolName=form.schoolName.data).first()
    if school_name:
        flash(f'{form.schoolName.data} Already Has An Entry! Click On Its Badge To Edit It.', category='danger')
        return redirect(request.url)
    else:
        if request.method == "POST":
            if form.validate_on_submit():
                name = form.schoolName.data
                af = form.appForm.data
                ff = form.feesForm.data
                if af and ff:
                    afName = secure_filename(af.filename)
                    ffName = secure_filename(ff.filename)
                    forms = Documents(schoolName=name, appForm=afName, appFormsPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], afName)), feesForm=ffName, feesFormsPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], ffName)))
                elif af:
                    afName = secure_filename(af.filename)
                    forms = Documents(schoolName=name, appForm=afName, appFormsPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], afName)))
                elif ff:
                    ffName = secure_filename(ff.filename)
                    forms = Documents(schoolName=name, feesForm=ffName, feesFormsPath=os.path.abspath(
                        os.path.join(app.config['UPLOAD_FOLDER'], ffName)))
                try:
                    db.session.add(forms)
                    db.session.commit()
                    flash(
                        f'Form(s) for {name} Have Been Uploaded Successfully.', category='success')
                    if af:
                        af.save(os.path.join(
                            app.config['UPLOAD_FOLDER'], afName))
                    if ff:
                        ff.save(os.path.join(
                            app.config['UPLOAD_FOLDER'], ffName))
                except:
                    db.session.rollback()
                    flash('There Was An Error While Uploading Form(s). Please Try Again Or Contact Administrator.',
                          category='danger')
                return redirect(request.url)
            else:
                flash(
                    'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
                return render_template('admin/add-school-forms.html', form=form)
        else:
            return render_template('admin/add-school-forms.html', form=form)


@ app.route('/admin/schools/delete/<string:name>')
@login_required
def delete_school(name):
    school = Schools.query.filter_by(schoolName=name).first()
    if school:
        db.session.delete(school)
        db.session.commit()
        os.remove(school.logoPath)
        os.remove(school.badgePath)

    images = Images.query.filter_by(schoolName=name).all()
    if images:
        if len(images) > 1:
            for pix in images:
                db.session.delete(pix)
                os.remove(pix.schoolPixPath)
            db.session.commit()
        else:
            db.session.delete(images)
            os.remove(images.schoolPixPath)
            db.session.commit()

    thumbs = Thumbnails.query.filter_by(name=name).all()
    if thumbs:
        if len(thumbs) > 1:
            for thumb in thumbs:
                db.session.delete(thumb)
                os.remove(thumb.vidPixPath)
            db.session.commit()
        else:
            db.session.delete(thumbs)
            os.remove(thumbs.vidPixPath)
            db.session.commit()

    docs = Documents.query.filter_by(schoolName=name).first()
    if docs:
        db.session.delete(docs)
        db.session.commit()
        if docs.appFormsPath:
            os.remove(docs.appFormsPath)
        if docs.feesFormsPath:
            os.remove(docs.feesFormsPath)
    return redirect(url_for('admin_schools'))


@ app.route('/admin/schools/edit/<string:name>', methods=["GET", "POST"])
@login_required
def edit_school(name):
    school = Schools.query.filter_by(schoolName=name).first()
    form = EditSchoolForm(obj=school)
    if request.method == "POST":
        if form.validate_on_submit():
            school.schoolName = form.schoolName.data
            school.country = form.country.data
            school.colour1 = form.colour1.data
            school.colour2 = form.colour2.data
            school.schType = form.schoolType.data
            school.population = form.population.data
            school.website = form.website.data
            school.address = form.address.data
            school.about = form.about.data
            school.facilities = form.facilities.data
            school.academics = form.academics.data
            school.extra = form.extra.data
            school.care = form.care.data
            school.newHeading = form.newHeading.data
            school.newBody = form.newBody.data
            school.newHeading2 = form.newHeading2.data
            school.newBody2 = form.newBody2.data
            school.newHeading3 = form.newHeading3.data
            school.newBody3 = form.newBody3.data
            school.link1 = form.link1.data
            school.link2 = form.link2.data
            school.link3 = form.link3.data
            school.link4 = form.link4.data
            school.link5 = form.link5.data
            school.tour = form.tour.data
            school.appLink = form.appLink.data
            school.feesLink = form.feesLink.data
            # school.logo = form.logo.data
            # school.badge = form.badge.data
            db.session.commit()
            flash(
                f'Information for {school.schoolName} Has Been Updated.', category='success')
            return redirect(url_for('admin_schools'))
        else:
            flash(
                f'Please Meet The Requirements For The Form Before Submiting It.', category='danger')
            return render_template('admin/edit-school.html', form=form, school=school)
    else:
        return render_template('admin/edit-school.html', form=form, school=school)


@ app.route('/admin/countries')
@login_required
def country():
    countries = Country.query.order_by(Country.id).all()
    return render_template('admin/countries.html', countries=countries)


@app.route('/admin/countries/add', methods=['POST'])
@login_required
def add_country():
    name = request.form['name']
    flag = request.files['flag']
    if flag:
        flagName = secure_filename(flag.filename)
        place = Country.query.filter_by(name=name).first()
        emblem = Country.query.filter_by(flag=flagName).first()
        if place:
            flash(f'{name} Already Exists! Please Enter A New Country.',
                  category='danger')
            return redirect(url_for('country'))
        elif emblem:
            flash(
                f'{flagName} Has Already Been Used For Another Country!', category='danger')
            return redirect(url_for('country'))
        else:
            new_country = Country(
                name=name, flag=flagName, flagPath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], flagName)))
            db.session.add(new_country)
            db.session.commit()
            flag.save(os.path.join(app.config['UPLOAD_FOLDER'], flagName))
            return redirect(url_for('country'))
    else:
        flash('No Country Image Found! Please Attach Image.', category='danger')
        return redirect(url_for('country'))


@ app.route('/admin/countries/delete/<int:id>')
@login_required
def delete_country(id):
    country = Country.query.get_or_404(id)
    db.session.delete(country)
    db.session.commit()
    filepath = country.flagPath
    os.remove(filepath)
    return redirect(url_for('country'))


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404


@ app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('pages/500.html'), 500
