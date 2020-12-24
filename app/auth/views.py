from flask import render_template, request, redirect, url_for,\
     session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Task, load_user
from ..mail import send_email
import time


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # 展示欢迎页
    is_visited = session.get('is_visited')
    if not is_visited:
        session['is_visited'] = True
        return redirect(url_for('main.welcome'))

    # 支持通过[邮箱]登录
    email = request.form.get('user')
    input_password = request.form.get('password')
    if email and input_password:
        # 在数据库中查询用户是否存在
        user = User.query.filter(User.email == email).first()
        if user and user.verify_password(input_password):
            login_user(user)
            session['known'] = True
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('main.index'))
        else:
            # flash('错误的用户名或密码')
            session['known'] = False
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('user_id', 'password', 'name'):
        session.pop(key, None)
    session['known'] = False
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    name = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    # 密码的一致性检查
    if name and password1 and password2:
        # 发送邮件
        email = request.form.get('email')
        # 不能已被注册
        if User.query.filter(User.email == email).first():
            return render_template('auth/register.html')
        # 注册用户
        user = User(name=name,
                    password=password1,
                    email=email)
        db.session.add(user)
        db.session.commit()
        # 添加初始 task
        task = Task(text='开始 DDL 管理之旅',
                    start_date=(time.strftime("%Y-%m-%d", time.localtime())),
                    duration=1,
                    progress=0.2,
                    parent=0,
                    open=True,
                    user_id=user.id)
        db.session.add(task)
        db.session.commit()
        # 发送验证邮件
        token = user.generate_confirmation_token()
        send_email(email, 'DDL Manager 注册验证',
                   'auth/email/confirm',
                   name=name, token=token)
        return redirect(url_for('auth.success'))
    return render_template('auth/register.html')


@auth.route('/confirm/<token>')
# @login_required
def confirm(token):
    if current_user.confirm(token):
        db.session.commit()
    return redirect(url_for('auth.success'))


@auth.route('/success')
def success():
    if not current_user.is_authenticated:
        # 说明该重定向自注册页面
        head = "注册成功！"
        mes1 = ' 我们已经向你的邮箱发送一封邮件'
        mes2 = '请通过邮件中的链接登录,以激活账户'
        skip = False
    else:
        # 说明重定向自验证页面
        head = "激活成功！"
        mes1 = '即将进入主页，请稍等...'
        mes2 = ''
        skip = True  # 等待3秒后跳转主页
    return render_template('auth/success.html',
                           head=head, mes1=mes1, mes2=mes2, skip=skip)


# ###########################
# 下面是用户信息的修改
# ###########################
@auth.route('/edit_headpic')
@login_required
def edit_headpic():
    user_id = session.get('user_id')
    user = load_user(user_id)
    avatar = request.files.get('avatar')
    if avatar:
        fname = avatar.filename
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
        flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        if not flag:
            return render_template('profile.html')
        # avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, user.name, fname))
        user.headpic = (UPLOAD_FOLDER + '{}_{}').format(user.id, fname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.profile'))


@auth.route('/edit_name')
@login_required
def edit_name():
    user_id = session.get('user_id')
    user = load_user(user_id)
    name = request.form.get('name')
    if name:
        user.name = name
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/edit_password')
@login_required
def edit_password():
    user_id = session.get('user_id')
    user = load_user(user_id)
    pwd = request.form.get('password')
    if pwd:
        user.name = pwd
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.profile'))
