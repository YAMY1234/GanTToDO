from flask import current_app
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_restful import marshal, marshal_with, fields


# #####################################
# 各任务之间的连接，表示task的先后关系
# #####################################
class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer)
    target = db.Column(db.Integer)
    type = db.Column(db.Integer)  # type:db.Column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def load(user_id):
        return Link.query.filter(Link.user_id == user_id).all()

    @staticmethod
    def from_json(json_link):
        source = json_link.get('source')
        target = json_link.get('target')
        type = json_link.get('type')
        return Link(source=source,
                    target=target,
                    type=type)

    def update(self, json_link):
        self.source = json_link.get('source')
        self.target = json_link.get('target')
        self.type = json_link.get('type')


# ###########################################
# gantt图所用的任务定义
# ###########################################
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    progress = db.Column(db.Float)
    parent = db.Column(db.Integer)
    open = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def from_json(json_task):
        text = json_task.get('text')
        date = json_task.get('start_date')
        # d-m-y转换为y-m-d（后端格式也可以设为d-m-y，但特意弄成不一致的）
        start_date = date[6:] + '-' + date[3:5] + '-' + date[0:2]
        duration = json_task.get('duration')
        progress = json_task.get('progress')
        parent = json_task.get('parent')
        # user_id = json_event('user_id')  # 用户id由api添加
        return Task(text=text,
                    start_date=start_date,
                    duration=duration,
                    progress=progress,
                    parent=parent,
                    open=True)

    @staticmethod
    def load(user_id):
        return Task.query.filter(Task.user_id == user_id).all()

    # 与from_json区别在于，update是改自己，from_json是新建
    def update(self, json_task):
        self.text = json_task.get('text')
        date = json_task.get('start_date')
        self.start_date = date[6:] + '-' + date[3:5] + '-' + date[0:2]
        self.duration = json_task.get('duration')
        self.progress = json_task.get('progress')
        self.parent = json_task.get('parent')
        self.open = json_task.get('open')


# ###########################################
# 用户模型
# ###########################################
class User(UserMixin, db.Model):
    __tablename__ = 'user'  # 数据库中的表名
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    # 头像文件名（账号）
    headpic = db.Column(db.String(128), default='default.png')
    # 注册日期
    # register_time = db.Column(db.DateTime(), default=datetime.utcnow)
    email = db.Column(db.String(64), unique=True, index=True)
    task = db.relationship('Task', backref='user', lazy='dynamic')
    link = db.relationship('Link', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except(Exception):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
