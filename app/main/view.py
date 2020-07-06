import os
from os import startfile

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required
from flask_uploads import UploadSet
from sqlalchemy import or_

from . import main
from .form import MovieForm
from ..model import MovieInfo
from ..utils import getGray, sortPoster


@main.route('/', methods = ['GET', 'POST'])
@main.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = MovieInfo.query.order_by(MovieInfo.id.desc()).paginate(page, 4, error_out=False)
    movies = pagination.items
    return render_template('index.html', pagination=pagination, movies=movies)

@main.route('/text-search', methods=['GET', 'POST'])
@login_required
def text_search():
    text = request.form.get('keyword')
    text = "" if text is None else text
    if text is "":
        return redirect(url_for('.index'))
    movies = MovieInfo.query.filter(or_(
        MovieInfo.moviename.like("%" + text + "%") if text is not None else "",
        MovieInfo.time.like("%" + text + "%") if text is not None else "",
        MovieInfo.actor.like("%" + text + "%") if text is not None else "",
        MovieInfo.director.like("%" + text + "%") if text is not None else "",
        MovieInfo.content.like("%" + text + "%") if text is not None else ""
    )).order_by(MovieInfo.id.desc()).all()
    return render_template('search.html', movies=movies, text=text)

@main.route('/picture-search', methods=['GET', 'POST'])
@login_required
def picture_search():
    picture = request.files.get('picture')
    if picture and picture.filename:
        picturePath = os.path.join(os.path.dirname(__file__), "../", "static", "tmp") + "/" + picture.filename
        picture.save(picturePath)
        uploadGray = getGray(picturePath)
        sqlList = MovieInfo.query.all()
        movies = sortPoster(uploadGray, sqlList)
        os.remove(picturePath)
        return render_template('search.html', movies=movies, text="")
    return redirect(url_for('.index'))


@main.route('/play/<id>', methods=['GET', 'POST'])
@login_required
def play(id):
    movie = MovieInfo.query.filter_by(id=id).first()
    path = os.path.join(os.path.dirname(__file__), "../") + movie.moviepath
    startfile(path)
    return redirect(url_for('.index'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = MovieForm()
    if form.validate_on_submit():
        posterPath = os.path.join('/static', 'poster', form.poster.data.filename)
        moviePath = os.path.join('/static', 'movie', form.movie.data.filename)

        UploadSet('POSTER').save(form.poster.data, name=form.poster.data.filename)
        UploadSet('MOVIE').save(form.movie.data, name=form.movie.data.filename)

        imageinfo = getGray(os.path.join(os.path.dirname(__file__), "../") + posterPath)
        MovieInfo.addMovie(form.movieName.data, form.time.data, form.director.data, form.actors.data, form.intro.data, posterPath, moviePath, imageinfo)
        flash('Your movie has been updated!')
        return redirect(url_for('.index'))
    return render_template('upload.html', form=form)

