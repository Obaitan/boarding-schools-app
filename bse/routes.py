import os

from bse import app, db, bcrypt, mail
from flask import render_template, url_for, redirect, request, flash, send_from_directory
from bse.models import News, User, Country, Schools, Images, Documents
from werkzeug.utils import secure_filename
from bse.forms import LoginForm, ContactForm, SchoolsForm, AgentsForm, SubmitDocsForm, BoardingSchoolsForm, ImageForm, DocumentsForm
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import exc



ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    countries = Country.query.order_by(Country.id).all()
    return render_template('pages/schools.html', countries=countries)


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
                'Please provide valid information for each field before clicking "SUBMIT FORM" again.', category='danger')
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

    elif request.method == 'GET':
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
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home'))


@app.route('/admin/dashboard')
# @login_required
def dashboard():
    return render_template('admin/admin-dashboard.html')


@app.route('/admin/news')
# @login_required
def dashboard_news():
    news = News.query.order_by(News.id.desc()).all()
    return render_template('admin/articles.html', news=news)


@app.route('/admin/news/add')
# @login_required
def new_article():
    return render_template('admin/add-article.html')


@app.route('/admin/schools')
# @login_required
def admin_schools():
    schools = Schools.query.order_by(Schools.id).all()
    return render_template('admin/admin-schools.html', schools=schools)


@app.route('/admin/schools/add/information', methods=['GET', 'POST'])
# @login_required
def new_school():
    form = BoardingSchoolsForm()
    form2 = ImageForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
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
            col2 = form.col2.data
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

            if 'logo' not in request.files:
                flash('No Image Data Found', category='danger')
                return redirect(request.url)
            logo = request.files['logo']
            if logo.filename == '':
                flash('No Image Selected', category='danger')
                return redirect(request.url)
            if logo and allowed_file(logo.filename):
                logoName = secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logoName))

            if 'badge' not in request.files:
                flash('No Image Data Found', category='danger')
                return redirect(request.url)
            badge = request.files['badge']
            if badge.filename == '':
                flash('No Image Selected', category='danger')
                return redirect(request.url)
            if badge and allowed_file(badge.filename):
                badgeName = secure_filename(badge.filename)
                badge.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], badgeName))

            new_school = Schools(
                colour1=col1, colour2=col2, schoolName=name, schoolType=schType, population=population, address=address, website=website, about=about, country=country, logo=logoName, logoPath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], logoName)), badge=badgeName, badgePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], badgeName)), facilities=facilities, academics=academics, extra=extra, care=care, newHeading=nH, newBody=nB, newHeading2=nH2, newBody2=nB2, newHeading3=nH3, newBody3=nB3, link1=link1, link2=link2, link3=link3, link4=link4, link5=link5)
            try:
                db.session.add(new_school)
                db.session.commit()
                flash(f'Information for {name} Has Been Saved. Please Upload Images And Forms Next.',
                      category='success')
            except exc.IntegrityError:
                db.session.rollback()
                flash('There Was An Error While Processing Form. Please Try Again Or Contact Administrator',
                  category='danger')
        return redirect(request.url)

    else:
        return render_template('admin/add-school.html', form=form, form2=form2)


@app.route('/admin/schools/add/images', methods=['GET', 'POST'])
# @login_required
def new_school2():
    form = BoardingSchoolsForm()
    form2 = ImageForm()
    if request.method == "POST":
        if form2.validate_on_submit():
            form.name.choices = [Schools.query.filter_by(country).al]            
            # files_filenames = []
            # for file in form.files.data:
            #     file_filename = secure_filename(file.filename)
            #     data.save(os.path.join(
            #         app.config['UPLOAD_FOLDER'], data_filename))
            #     files_filenames.append(file_filename)
            # print(files_filenames)

            if 'schoolPix[]' not in request.files:
                flash('Images Missing! Please Upload School Images',
                      category='danger')
                return redirect(request.url)
            schoolPix = request.files.getlist('schoolPix[]')
            for pix in schoolPix:
                if pix and allowed_file(pix.filename):
                    schPixName = secure_filename(pix.filename)
                    pix.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], schPixName))
            
            if 'vidPix[]' not in request.files:
                flash('Images Missing! Please Upload School Images',
                      category='danger')
                return redirect(request.url)
            vidPix = request.files.getlist('vidPix[]')
            for img in vidPix:
                if img and allowed_file(img.filename):
                    imgName = secure_filename(img.filename)
                    img.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], imgName))
            
            schImages = Images(schoolName=name, schoolPix=schoolPix, schoolPixPath=os.path.abspath(
                os.path.join(app.config['UPLOAD_FOLDER'], schPixName)), vidPix=vidPix, vidThumbnailPath=os.path.abspath(
                os.path.join(app.config['UPLOAD_FOLDER'], imgName)))
            try:
                db.session.add(schImages)
                db.session.commit()
                flash(f'Images for {name} Have Been Saved. Please Upload Forms/Links Next.',
                      category='success')
            except exc.IntegrityError:
                db.session.rollback()
                flash('There Was An Error While Processing Form. Please Try Again Or Contact Administrator',
                      category='danger')
            return redirect(request.url)
            
    return render_template('admin/add-school.html', form=form, form2=form2)


@app.route('/upload_article', methods=['GET', 'POST'])
# @login_required
def upload_article():
    if request.method == "POST":
        news_title = request.form['title']
        news_author = request.form['author']
        news_excerpt = request.form['excerpt']
        news_article = request.form['article']

        # check if the post request has the file part
        if 'thumbnail' not in request.files:
            flash('No file part')
            return redirect(request.url)
        thumbnail = request.files['thumbnail']
        if thumbnail.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if thumbnail and allowed_file(thumbnail.filename):
        filename = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = News(
            title=news_title, excerpt=news_excerpt, article=news_article, author=news_author, thumbnail=filename, imagePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard_news'))
    else:
        return render_template('admin/articles.html')


@app.route('/admin/country/add', methods=['GET', 'POST'])
# @login_required
def add_country():
    if request.method == "POST":
        country_name = request.form['name']

        # check if the post request has the file part
        if 'flag' not in request.files:
            flash('No file part')
            return redirect(request.url)
        flag = request.files['flag']
        if flag.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if thumbnail and allowed_file(thumbnail.filename):
        filename = secure_filename(flag.filename)
        flag.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_country = Country(
            name=country_name, flagName=filename, imagePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        db.session.add(new_country)
        db.session.commit()
        return redirect(url_for('country'))
    else:
        return render_template('admin/countries.html')


@app.route('/admin/country/delete/<int:id>')
def delete_country(id):
    countries = Country.query.get_or_404(id)
    filepath = countries.imagePath
    os.remove(filepath)
    db.session.delete(countries)
    db.session.commit()
    return redirect(url_for('country'))


@app.route('/static/uploads/<filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/admin/countries')
# @login_required
def country():
    countries = Country.query.order_by(Country.id).all()
    return render_template('admin/countries.html', countries=countries)


@app.route('/news/article')
def article():
    return render_template('news/single-article.html', news=news)


@app.route('/admin/news/delete/<int:id>')
def delete_article(id):
    news = News.query.get_or_404(id)
    filepath = news.imagePath
    os.remove(filepath)
    db.session.delete(news)
    db.session.commit()
    return redirect('/admin/news')


@app.route('/admin/news/edit/<int:id>', methods=["GET", "POST"])
# @login_required
def edit_article(id):
    news = News.query.get_or_404(id)
    if request.method == "POST":
        news.title = request.form['title']
        news.excerpt = request.form['excerpt']
        news.article = request.form['article']
        news.author = request.form['author']

        # check if the post request has the file part
        if 'thumbnail' not in request.files:
            flash('No file part')
            return redirect(request.url)
        thumbnail = request.files['thumbnail']
        if thumbnail.filename == '':
            flash('No image file selected. Please select an image file.',
                  category='danger')
            return redirect(request.url)
        # if thumbnail and allowed_file(thumbnail.filename):
        filename = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        news.thumbnail = filename
        news.imagePath = os.path.abspath(
            os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.commit()
        return redirect('/admin/news')
    else:
        # filepath = news.fp
        # os.remove(filepath)
        return render_template('admin/edit-article.html', news=news)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('pages/500.html'), 500

