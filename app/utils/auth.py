from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import datetime
from app.models import UserInfo
import jwt
from django.conf import settings
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed
class JWT_authentication(BaseAuthentication):
    '''
    jwt认证
    '''
    def authenticate(self,request):
        token = request.data['token']
        salt = settings.SECRET_KEY
        payload = None
        try:
            payload = jwt.decode(token,salt,True)  # True表示认证，返回值是payload
        except exceptions.ExpiredSignature:
            raise AuthenticationFailed({'code':40002,'error':'token失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code':40003,'error':'token认真失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code':40004,'error':'非法的token'})
        if not payload:
            return (payload,token)


def jwt_produce():   #  生成JWT Token
    salt = settings.SECRET_KEY
    # header是默认的
    # headers = {
    #     'typ':'jwt',
    #     'alg':'HS256'
    # }

    # 构造payload
    #  
    payload = {
        'user_id':10010,
        'user_name':'admin',
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)
    }
    token = jwt.encode(payload=payload,key=salt)
    return token

class My_authentication(BaseAuthentication):
    def authenticate(self, request):

        # 前端需要传入'auth':[value]的键值对用户认证
        auth = request.META.get('HTTP_AUTH', None)  # type: str

        if auth is None:  # 游客
            return None
        auth_list = auth.split()
        if len(auth_list) != 2 or auth_list[0] != 'auth':
            raise AuthenticationFailed('非法认证信息')

        # todo 解析认证信息，得到用户名，简单起见，直接找username为'超级会员'的用户
        # if auth_list[1] == 'HUB':  # 解析认证信息
        user = UserInfo.objects.filter(username='超级会员').first()

        if not user:
            raise AuthenticationFailed('认证失败')
        return (user, None)
