from bse import app, db
from flask import render_template, url_for, redirect, request
from bse.models import News
from werkzeug.utils import secure_filename

import os


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
    return render_template('pages/schools.html')


@app.route('/agents')
def agents():
    return render_template('pages/agents.html')


@app.route('/contact')
def contact():
    return render_template('pages/contact.html')


@app.route('/admin')
def admin():
    return render_template('admin/admin-login.html')


@app.route('/admin/dashboard')
def dashboard():
    return render_template('admin/admin-dashboard.html')


@app.route('/admin/dashboard/news')
def dashboard_news():
    news = News.query.order_by(News.id).all()
    return render_template('admin/edit-article.html', news=news)


@app.route('/news')
def news():
    news = News.query.order_by(News.id).all()
    return render_template('news/news-page.html', news=news)


@app.route('/new_article')
def new_article():
    return render_template('admin/add-article.html')


@app.route('/upload_article', methods=['GET', 'POST'])
def upload_article():
    if request.method == "POST":
        news_title = request.form['title']
        news_author = request.form['author']
        news_excerpt = request.form['excerpt']
        news_article = request.form['article']
        thumbnail = request.files['thumbnail']

        if not thumbnail:
            return 'No thumbnail image uploaded', 400

        filename = secure_filename(thumbnail.filename)
        mimetype = thumbnail.mimetype

        new_post = News(
            title=news_title, excerpt=news_excerpt, article=news_article, author=news_author, thumbnail=thumbnail.read(), mimetype=mimetype, name=filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/admin/dashboard/news')
    else:
        return render_template('news/news_page.html')


@app.route('/news/article')
def article():
    return render_template('news/single-article.html', news=news)


@app.route('/admin/dashboard/news/delete/<int:id>')
def delete_article(id):
    news = News.query.order_by(News.id).all()
    db.session.delete(news)
    db.session.commit()
    return redirect('/admin/dashboard/news')


@app.route('/admin/dashboard/news/edit/<int:id>', methods=["GET", "POST"])
def edit_article(id):
    news = News.query.order_by(News.id).all()
    if request.method == "POST":
        news.title = request.form['title']
        news.excerpt = request.form['excerpt']
        news.article = request.form['article']
        news.author = request.form['author']
        thumbnail = request.files['thumbnail']
        db.session.commit()
        return redirect('/admin/dashboard/news')
    else:
        return render_template('admin/edit-article.html', news=news)
