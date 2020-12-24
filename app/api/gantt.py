from flask import request, session  # , json
from .. import db
from ..models import Task, Link
from . import api
# from ..main.func import JSONHelper


# @api.route('/data', methods=['GET'])
# def load_data():
#     user_id = session.get('user_id')
#     task = Task.query.filter(Task.user_id == user_id).all()
#     link = Link.query.filter(Link.user_id == user_id).all()
#     return json_data


@api.route('/data/task', methods=['POST'])
def add_task():
    re = request.json
    task = Task.from_json(re)
    task.user_id = session.get('user_id')  # 用g变量为佳
    db.session.add(task)
    db.session.commit()
    return {"action": "inserted", "tid": str(task.id)}


@api.route('/data/task/<int:tid>', methods=['PUT'])
def edit_task(tid):
    re = request.json
    re.pop('end_date')
    task = Task.query.filter(Task.id == int(tid)).first()
    if not task:
        return {"action": "no task"}
    task.update(re)
    db.session.add(task)
    db.session.commit()
    return {"action": "updated"}


@api.route('/data/task/<int:tid>', methods=['DELETE'])
def del_task(tid):
    task = Task.query.filter(Task.id == int(tid)).first()
    if not task:
        return {"action": "no task"}
    db.session.delete(task)
    db.session.commit()
    return {"action": "deleted"}


@api.route('/data/link', methods=['POST'])
def add_link():
    re = request.json
    print(re)
    link = Link.from_json(re)
    link.user_id = session.get('user_id')  # 用g变量为佳
    db.session.add(link)
    db.session.commit()
    return {"action": "inserted", "lid": str(link.id)}


@api.route('/data/link/<int:lid>', methods=['PUT'])
def edit_link(lid):
    re = request.json
    link = Link.query.filter(Link.id == int(lid)).first()
    if not link:
        return {"action": "no link"}
    link.update(re)
    db.session.add(link)
    db.session.commit()
    return {"action": "updated"}


@api.route('/data/link/<int:lid>', methods=['DELETE'])
def del_link(lid):
    link = Link.query.filter(Link.id == int(lid)).first()
    if not link:
        return {"action": "no link"}
    db.session.delete(link)
    db.session.commit()
    return {"action": "deleted"}
