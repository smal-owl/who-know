from flask import Flask, render_template
from flask_login import LoginManager
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)

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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    add_news()
    app.run(port=8080, host='127.0.0.1')