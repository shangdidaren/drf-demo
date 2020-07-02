from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app.models import UserInfo


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
