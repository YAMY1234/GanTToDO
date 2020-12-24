# 数据库初始化，只用运行一次；与其他.py相对独立
# 为用户资料数据库创建一些测试数据
# 注：大量数据的建立应通过 .sql 完成

import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import config  # 从config读取配置

app = flask.Flask(__name__)
app.config.from_object(config['default'])
config['default'].init_app(app)
db = SQLAlchemy(app)


# ###################################
# 与程序top独立，不能从models引入
# ###################################
class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer)
    target = db.Column(db.Integer)
    type = db.Column(db.Integer)  # type:db.Column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    def from_json(json_event):
        text = json_event.get('text')
        start_date = json_event.get('start_date')
        duration = json_event.get('duration')
        progress = json_event.get('progress')
        parent = json_event.get('parent')
        # user_id = json_event('user_id')  # 用户id由api添加
        return Task(text=text,
                    start_date=start_date,
                    duration=duration,
                    progress=progress,
                    open=True,
                    parent=parent)


class User(UserMixin, db.Model):
    __tablename__ = 'user'  # 数据库中的表名
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    # 头像文件名（即账号）
    headpic = db.Column(db.String(128), default='default.jpg')
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


if __name__ == '__main__':
    db.drop_all()  # 销毁原数据库
    db.create_all()

    # ###############################################
    # 下列操作为数据库建立样例数据
    # 直观的相互关系，只需登录信小安账号查看即可（密码如下）
    # ###############################################
    # 新建用户
    user_alice = User(name='信小安',
                      password='123456',
                      headpic='1.jpg',
                      email='test1@qq.com',
                      confirmed=True
                      )
    user_bob = User(name='小明',
                    password='654321',
                    email='test2@tongji.edu.cn',
                    confirmed=True
                    )

    # 新建事件
    alice_task_1 = Task(text='大作业1', start_date='2020-12-18', duration=18,
                        parent=0, progress=0.4, open=True,
                        user=user_alice
                        )
    alice_task_2 = Task(text='大作业2', start_date='2020-12-14', duration=11,
                        parent=0, progress=0.6, open=True,
                        user=user_alice
                        )

    db.session.add_all([alice_task_1, alice_task_2])
    db.session.commit()  # 先提交生成id，以便作为子事件的id

    alice_task_1_1 = Task(text='事项 1', start_date='2020-12-19', duration=8,
                          parent=alice_task_1.id, progress=0.5, open=True,
                          user=user_alice
                          )

    alice_task_1_2 = Task(text='事项 2', start_date='2020-12-19', duration=8,
                          parent=alice_task_1.id, progress=0.5, open=True,
                          user=user_alice
                          )

    alice_task_1_3 = Task(text='事项 3', start_date='2020-12-30', duration=6,
                          parent=alice_task_1.id, progress=0.5, open=True,
                          user=user_alice
                          )
    db.session.add_all([alice_task_1_1, alice_task_1_2, alice_task_1_3])
    db.session.commit()  # 先提交生成id，以便作为子事件的id

    alice_task_1_1_1 = Task(text='子事项 1', start_date='2020-12-19', duration=7,
                            parent=alice_task_1_1.id, progress=0.6, open=True,
                            user=user_alice
                            )

    alice_task_1_1_2 = Task(text='子事项 2', start_date='2020-12-20', duration=7,
                            parent=alice_task_1_1.id, progress=0.6, open=True,
                            user=user_alice
                            )

    alice_task_1_2_1 = Task(text='子事项 1', start_date='2020-12-28', duration=8,
                            parent=alice_task_1_2.id, progress=0.6, open=True,
                            user=user_alice
                            )

    alice_task_1_3_1 = Task(text='子事项 1', start_date='2020-12-31', duration=5,
                            parent=alice_task_1_3.id, progress=0.5, open=True,
                            user=user_alice
                            )

    alice_task_1_3_2 = Task(text='子事项 2', start_date='2020-12-31', duration=4,
                            parent=alice_task_1_3.id, progress=0.5, open=True,
                            user=user_alice
                            )

    alice_task_1_3_3 = Task(text='子事项 3', start_date='2020-12-31', duration=3,
                            parent=alice_task_1_3.id, progress=0.5, open=True,
                            user=user_alice
                            )

    db.session.add_all([alice_task_1_1_1, alice_task_1_1_2, alice_task_1_2_1,
                        alice_task_1_3_1, alice_task_1_3_2, alice_task_1_3_3])
    db.session.commit()

    alice_task_2_1 = Task(text='事项 1', start_date='2020-12-20', duration=5,
                          parent=alice_task_2.id, progress=1, open=True,
                          user=user_alice
                          )

    alice_task_2_2 = Task(text='事项 2', start_date='2020-12-19', duration=7,
                          parent=alice_task_2.id, progress=0.5, open=True,
                          user=user_alice
                          )

    alice_task_2_3 = Task(text='事项 3', start_date='2020-12-19', duration=6,
                          parent=alice_task_2.id, progress=0.8, open=True,
                          user=user_alice
                          )

    alice_task_2_4 = Task(text='事项 4', start_date='2020-12-19', duration=5,
                          parent=alice_task_2.id, progress=0.2, open=True,
                          user=user_alice
                          )

    alice_task_2_5 = Task(text='事项 2', start_date='2020-12-19', duration=7,
                          parent=alice_task_2.id, progress=0, open=True,
                          user=user_alice
                          )

    db.session.add_all([alice_task_2_1, alice_task_2_2, alice_task_2_3,
                        alice_task_2_4, alice_task_2_5])
    db.session.commit()

    alice_task_2_2_1 = Task(text='子事项 1', start_date='2020-12-20', duration=2,
                            parent=alice_task_2_2.id, progress=1, open=True,
                            user=user_alice
                            )

    alice_task_2_2_2 = Task(text='子事项 2', start_date='2020-12-23', duration=3,
                            parent=alice_task_2_2.id, progress=0.8, open=True,
                            user=user_alice
                            )

    alice_task_2_2_3 = Task(text='子事项 3', start_date='2020-12-27', duration=4,
                            parent=alice_task_2_2.id, progress=0.2, open=True,
                            user=user_alice
                            )

    alice_task_2_2_4 = Task(text='子事项 4', start_date='2020-12-27', duration=4,
                            parent=alice_task_2_2.id, progress=0, open=True,
                            user=user_alice
                            )

    db.session.add_all([alice_task_2_2_1, alice_task_2_2_2, alice_task_2_2_3,
                        alice_task_2_2_4])
    db.session.commit()

    alice_link_1_11 = Link(source=alice_task_1.id, target=alice_task_1_1.id,
                           type=1, user=user_alice
                           )

    alice_link_11_12 = Link(source=alice_task_1_1.id, target=alice_task_1_2.id,
                            type=0, user=user_alice
                            )

    alice_link_12_13 = Link(source=alice_task_1_2.id, target=alice_task_1_3.id,
                            type=0, user=user_alice
                            )

    alice_link_11_111 = Link(source=alice_task_1_1.id, target=alice_task_1_1_1.id,
                             type=2, user=user_alice
                             )

    alice_link_11_112 = Link(source=alice_task_1_1.id, target=alice_task_1_1_2.id,
                             type=2, user=user_alice
                             )

    alice_link_12_121 = Link(source=alice_task_1_2.id, target=alice_task_1_2_1.id,
                             type=2, user=user_alice
                             )

    alice_link_13_131 = Link(source=alice_task_1_3.id, target=alice_task_1_3_1.id,
                             type=2, user=user_alice
                             )

    alice_link_13_132 = Link(source=alice_task_1_3.id, target=alice_task_1_3_2.id,
                             type=2, user=user_alice
                             )

    alice_link_13_133 = Link(source=alice_task_1_3.id, target=alice_task_1_3_3.id,
                             type=2, user=user_alice
                             )

    db.session.add_all([alice_link_1_11, alice_link_11_12, alice_link_12_13,
                        alice_link_11_111, alice_link_11_112, alice_link_12_121,
                        alice_link_13_131, alice_link_13_132, alice_link_13_133])
    db.session.commit()

    alice_link_2_21 = Link(source=alice_task_2.id, target=alice_task_2_1.id,
                           type=1, user=user_alice
                           )

    alice_link_2_22 = Link(source=alice_task_2.id, target=alice_task_2_2.id,
                           type=1, user=user_alice
                           )

    alice_link_2_23 = Link(source=alice_task_2.id, target=alice_task_2_3.id,
                           type=1, user=user_alice
                           )

    alice_link_2_24 = Link(source=alice_task_2.id, target=alice_task_2_4.id,
                           type=1, user=user_alice
                           )

    alice_link_2_25 = Link(source=alice_task_2.id, target=alice_task_2_5.id,
                           type=1, user=user_alice
                           )

    alice_link_22_221 = Link(source=alice_task_2_2.id, target=alice_task_2_2_1.id,
                             type=1, user=user_alice
                             )

    alice_link_221_222 = Link(source=alice_task_2_2_1.id, target=alice_task_2_2_2.id,
                              type=0, user=user_alice
                              )

    alice_link_222_223 = Link(source=alice_task_2_2_2.id, target=alice_task_2_2_3.id,
                              type=0, user=user_alice
                              )

    alice_link_223_224 = Link(source=alice_task_2_2_3.id, target=alice_task_2_2_4.id,
                              type=0, user=user_alice
                              )

    db.session.add_all([alice_link_2_21, alice_link_2_22, alice_link_2_23,
                        alice_link_2_24, alice_link_2_25, alice_link_22_221,
                        alice_link_221_222, alice_link_222_223, alice_link_223_224])
    db.session.commit()

    bob_task_1 = Task(text='小明的生日', start_date='2021-01-01', duration=18,
                      parent=0, progress=0.4, open=True,
                      user=user_bob
                      )
    db.session.add(bob_task_1)
    db.session.commit()
    # app.run()
    print('数据库初始化完成')
