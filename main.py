from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from waitress import serve
from werkzeug.utils import redirect

from flask_restful import reqparse, abort, Api, Resource

import data.users_resource as us_re

from data import db_session, news_resources, quests_resource
from data.users import User
from data.news import News
from data.quests import Quest
from forms.user import RegisterForm
from forms.LoginForm import LoginForm
from forms.news import NewsForm
from forms.questsForm import QuestsForm
import datetime

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


def add_quest():
    quest = Quest()
    quest.content = "биография пользователя 1"
    db_sess = db_session.create_session()
    db_sess.add(quest)
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


#  Тест

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/news', methods=['GET', 'POST'])
@login_required

def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/tasks')
    return render_template('news.html', title='Добавление новости',
                           form=form)

'''def add_news():
    form = NewsForm()
    if request.method == 'GET':
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = News()
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            current_user.news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/tasks')
    elif request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        with open(f'static/img/{f.filename}', 'wb') as file:
            print(f.filename)
            file.write(f.read())
    return render_template('news.html', title='Добавление новости',
                       form=form)
'''

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form_news = NewsForm()
    form_quest = QuestsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id
                                          ).first()

        quest = db_sess.query(Quest).filter(Quest.news_id == id)

        if news:
            form_news.title.data = news.title
            form_news.content.data = news.content
            form_news.is_private.data = news.is_private

        else:
            abort(404)

        #  if quest:
        #      form_quest.content.data = quest.content

    if form_news.validate_on_submit():
        print('Зашёл в валидатор у News')
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id
                                          ).first()
        if news:
            news.title = form_news.title.data
            news.content = form_news.content.data
            news.is_private = form_news.is_private.data
            db_sess.commit()
            return redirect('/tasks')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form_news
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/tasks')


@app.route('/quest/<int:id>', methods=['GET', 'POST'])
@login_required
def quest(id):
    form = QuestsForm()
    if request.method == "GET":
        print('Зашёл в метод GET')
        db_sess = db_session.create_session()
        quest = db_sess.query(Quest).filter(Quest.id == id
                                            ).first()
        if quest:
            print('Зашёл в проверку if quest внутри GET')
            form.content.data = quest.content
            form.user_id.data = quest.user_id
        else:
            print('Зашёл в проверку else внутри GET')
            abort(404)

    print('Вышел из GET')

    print(form.validate_on_submit())

    if form.validate_on_submit():
        print('Зашёл в валидатор')
        db_sess = db_session.create_session()
        quest = db_sess.query(Quest).filter(Quest.id == id
                                            ).first()
        if quest:
            quest.content = form.content.data
            quest.user_id = form.user_id.data
            db_sess.commit()
            return redirect('/tasks')
        else:
            abort(404)
    return render_template('quest.html',
                           title='Отправить ответ',
                           form=form
                           )


@app.route('/quests/<int:id>', methods=['GET', 'POST'])
@login_required
def add_quest(id):
    form = QuestsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quest = Quest()
        quest.content = form.content.data
        quest.news_id = id
        print(quest.content, id, sep='\n')
        current_user.quest.append(quest)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/tasks')
    return render_template('quest.html', title='Добавление Комментария',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/tasks")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    quest = db_sess.query(Quest)
    return render_template("tasks.html", news=news, quest=quest)


@app.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    db_sess = db_session.create_session()
    quest = db_sess.query(Quest).filter(Quest.news_id == id)
    return render_template("comment.html", news=quest)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

    api.add_resource(quests_resource.QuestListResource, '/api/v2/quest')

    api.add_resource(quests_resource.QuestResource, '/api/v2/quest/<int:news_id>')

    api.add_resource(us_re.UsersListResource, '/api/v2/users')

    api.add_resource(us_re.UsersResource, '/api/v2/users/<int:user_id>')

    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
"""    serve(app, host='0.0.0.0', port=5000)"""
