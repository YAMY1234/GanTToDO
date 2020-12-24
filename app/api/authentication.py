# 初始化Flask-HTTPAuth（未启用）
from flask import g  # g为预留容器，可以存储自定义的数据，每次请求会重置
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized

auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    pass


# #########################
# 采用简单的认证方式
#
# #########################
@auth.verify_password
def verify_password(user_id, password):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')
