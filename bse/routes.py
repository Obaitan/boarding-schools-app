import os

from bse import app, db
from flask import render_template, url_for, redirect, request, flash, send_from_directory
from bse.models import News, Admin, Country, School
from werkzeug.utils import secure_filename
from bse.forms import LoginForm
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home():
    news = News.query.order_by(News.id).all()
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


@app.route('/agents')
def agents():
    return render_template('pages/agents.html')


@app.route('/contact')
def contact():
    return render_template('pages/contact.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(
                f'There was an error in loging in: {err_msg}', category='danger')
    return render_template('admin/admin-login.html', form=form)


@app.route('/admin/dashboard')
def dashboard():
    return render_template('admin/admin-dashboard.html')


@app.route('/admin/dashboard/news')
def dashboard_news():
    news = News.query.order_by(News.id).all()
    return render_template('admin/articles.html', news=news)


@app.route('/news')
def news():
    news = News.query.order_by(News.id).all()
    return render_template('news/news-page.html', news=news)


@app.route('/new_article')
def new_article():
    return render_template('admin/add-article.html')


@app.route('/admin/dashboard/schools/add')
def new_school():
    return render_template('admin/add-school.html')


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_article', methods=['GET', 'POST'])
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
            title=news_title, excerpt=news_excerpt, article=news_article, author=news_author, name=filename, fp=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard_news'))
    else:
        return render_template('admin/articles.html')


@app.route('/admin/dashboard/country/add', methods=['GET', 'POST'])
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
            name=country_name, imageName=filename, imagePath=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        db.session.add(new_country)
        db.session.commit()
        return redirect(url_for('country'))
    else:
        return render_template('admin/countries.html')


@app.route('/admin/dashboard/country/delete/<int:id>')
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


@app.route('/admin/dashboard/countries')
def country():
    countries = Country.query.order_by(Country.id).all()
    return render_template('admin/countries.html', countries=countries)


@app.route('/news/article')
def article():
    return render_template('news/single-article.html', news=news)


@app.route('/admin/dashboard/news/delete/<int:id>')
def delete_article(id):
    news = News.query.get_or_404(id)
    filepath = news.fp
    os.remove(filepath)
    db.session.delete(news)
    db.session.commit()
    return redirect('/admin/dashboard/news')


@app.route('/admin/dashboard/news/edit/<int:id>', methods=["GET", "POST"])
def edit_article(id):
    news = News.query.get_or_404(id)
    if request.method == "POST":
        news.title = request.form['title']
        news.excerpt = request.form['excerpt']
        news.article = request.form['article']
        news.author = request.form['author']
        news.thumbnail = request.files['thumbnail']
        db.session.commit()
        return redirect('/admin/dashboard/news')
    else:
        # filepath = news.fp
        # os.remove(filepath)
        return render_template('admin/edit-article.html', news=news)
