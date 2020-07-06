from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    movieName = StringField('电影名称', validators = [DataRequired()])
    time = StringField('上映时间')
    director = StringField('导演')
    actors = StringField('演员')

    intro = TextAreaField('简介')

    poster = FileField('海报上传', validators=[FileAllowed(UploadSet('POSTER', IMAGES), '仅支持图片格式!'), FileRequired()])
    movie = FileField("电影上传", validators=[FileAllowed(UploadSet('MOVIE', ['mp4', 'avi']), '仅支持视频格式!'), FileRequired()])

    submit = SubmitField('提交')

