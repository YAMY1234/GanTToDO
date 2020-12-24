from .func import JSONHelper
from flask_login import login_required
from ..models import load_user, Task, Link
from . import main
from flask import render_template, session, json, redirect, url_for


@main.route('/welcome', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session.get('user_id')
    user = load_user(user_id)
    task = Task.load(user_id)  # 加载所有task，因此还是使用用户id搜索
    link = Link.load(user_id)
    return render_template(
        'homepage.html', user=user,
        data_json=json.dumps(JSONHelper.jsonBQlist(task), ensure_ascii=False),
        links_json=json.dumps(JSONHelper.jsonBQlist(link), ensure_ascii=False))


@main.route('/gantt', methods=['GET', 'POST'])
@login_required
def gantt():
    # 也可以走api(falsk-restful可用)
    user_id = session.get('user_id')
    user = load_user(user_id)
    task = Task.load(user_id)
    link = Link.load(user_id)
    return render_template(
        'gantt.html',
        headpic=user.headpic,
        data_json=json.dumps(JSONHelper.jsonBQlist(task), ensure_ascii=False),
        links_json=json.dumps(JSONHelper.jsonBQlist(link), ensure_ascii=False))


# ######################
# 下面是一些嵌套网页的处理
# ######################
@main.route("/homepage.html", methods=['GET'])
@login_required
def homepage():
    return redirect(url_for('main.index'))


@main.route('/profile.html', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    user = load_user(user_id)
    return render_template('profile.html',
                           name=user.name, headpic=user.headpic)


@main.route("/todo_list.html", methods=['GET'])
@login_required
def todo_list():
    return render_template("todo_list.html")


@main.route("/clock.html", methods=['GET'])
@login_required
def clock():
    return render_template("clock.html")


@main.route("/gantt.html", methods=['GET'])
@login_required
def gantt2():
    return redirect(url_for('main.gantt'))


@main.route("/tomato.html", methods=['GET'])
@login_required
def tomato():
    return render_template("tomato.html")
