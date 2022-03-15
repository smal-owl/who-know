from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.utils import redirect

from flask_restful import reqparse, abort, Api, Resource

from data import db_session, news_resources
from data.users import User
from data.news import News
from forms.user import RegisterForm

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def add_user():
    user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "fls;ds@gmail.com"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_news():
    news = News()
    news.title = "Пользователь 1"
    news.content = "биография пользователя 1"
    news.is_private = False
    db_sess = db_session.create_session()
    db_sess.add(news)
    db_sess.commit()


@app.route('/')
def main_window():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    # для списка объектов
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    # для одного объекта
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
