from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from teacher_app.models import User


class MyAuth(BaseAuthentication):

    def authenticate(self, request):
        # 获取认证信息
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        print(auth)
        if auth is None:
            return None

        # 设置认证信息的校验规则  "auth 认证信息"
        auth_split = auth.split()

        # 校验规则
        if not (len(auth_split) == 2 and auth_split[0].lower() == "auth"):
            raise exceptions.AuthenticationFailed("认证信息有误，认证失败")

        # 如果认证成功，开始解析用户  规定用户信息必须是 abc.admin.123
        if auth_split[1] != "Teacher.admin.123":
            raise exceptions.AuthenticationFailed("用户信息认证失败")

        # 校验数据库是否存在此用户
        user = User.objects.filter(username="kuro").first()

        if not user:
            raise exceptions.AuthenticationFailed("用户不存在或者已删除")

        return user, None
