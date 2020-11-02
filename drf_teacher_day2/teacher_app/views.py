from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
# Create your views here.
from teacher_app.models import Teacher, TUser
from teacher_app.serializers import TeacherSerializer, TeacherDeSerializer, TeacherModelSerializer, UserModelSerializer
from teacher_app.authentications import MyAuth
from teacher_app.permission import MyPermission
from teacher_app.throttle import SendMessageRate

class TeacherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        teacher_id = kwargs.get("id")
        if teacher_id:
            teacher_obj = Teacher.objects.get(pk=teacher_id)
            choose_teacher = TeacherModelSerializer(teacher_obj).data
            return Response({
                "status": 200,
                "message": "查询单个教师成功",
                "results": choose_teacher
            })
        else:
            all_the_teachers = Teacher.objects.all()
            all_teachers = TeacherModelSerializer(all_the_teachers, many=True).data
            return Response({
                "status": 200,
                "message": "查询全体教师成功",
                "results": all_teachers
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 400,
                "message": "出错了,请尽快处理!"
            })
        post_serializer = TeacherDeSerializer(data=request_data)
        # print(post_serializer)
        if post_serializer.is_valid():
            add_teacher = post_serializer.save()
            return Response({
                "status": 200,
                "message": "教师添加成功",
                "results": TeacherModelSerializer(add_teacher).data
            })
        else:
            return Response({
                "status": 400,
                "message": "教师添加失败",
                # 保存失败的信息会包含在 .errors中
                "results": post_serializer.errors
            })

    def delete(self, request, *args, **kwargs):
        teacher_id = kwargs.get("id")
        if teacher_id:
            try:
                user_del = Teacher.objects.get(id=teacher_id)
            except Teacher.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": '教师不存在'
                })

            choose_teacher = TeacherModelSerializer(user_del).data
            teacher_name = choose_teacher.get("username")
            user_del.delete()
            return Response({
                "status": 200,
                "message": "删除单个用户成功",
                "results": "删除用户id为" + teacher_name
            })
        else:
            return Response({
                "status": 400,
                "message": "删除失败",
            })

    def put(self, request, *args, **kwargs):
        # 整体修改单个: 修改一个对象的全部字段
        request_data = request.data
        teacher_id = kwargs.get("id")
        try:
            teacher_obj = Teacher.objects.get(pk=teacher_id)
        except Teacher.DoesNotExist:
            return Response({
                "status": 400,
                "message": '教师不存在'
            })
        put_serializer = TeacherModelSerializer(data=request_data, instance=teacher_obj)
        if put_serializer.is_valid():
            modify_teacher = put_serializer.save()
            return Response({
                "status": 200,
                "message": "修改单个教师全部字段成功",
                "results": TeacherModelSerializer(modify_teacher).data
            })
        else:
            return Response({
                "status": 400,
                "message": "修改单个教师全部字段失败",
                # 保存失败的信息会包含在 .errors中
                "results": put_serializer.errors
            })

    def patch(self, request, *args, **kwargs):
        # 整体修改单个: 修改一个对象的全部字段
        request_data = request.data
        teacher_id = kwargs.get("id")
        try:
            teacher_obj = Teacher.objects.get(pk=teacher_id)
        except Teacher.DoesNotExist:
            return Response({
                "status": 400,
                "message": '教师不存在'
            })
        put_serializer = TeacherModelSerializer(data=request_data, instance=teacher_obj, partial=True)
        if put_serializer.is_valid():
            modify_teacher = put_serializer.save()
            return Response({
                "status": 200,
                "message": "修改单个教师部分字段成功",
                "results": TeacherModelSerializer(modify_teacher).data
            })
        else:
            return Response({
                "status": 400,
                "message": "修改单个教师部分字段失败",
                # 保存失败的信息会包含在 .errors中
                "results": put_serializer.errors
            })


class TeacherGenericAPIView(GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    queryset = Teacher.objects.filter()
    serializer_class = TeacherModelSerializer

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.


class UserViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = TUser.objects.all()
    serializer_class = UserModelSerializer

    def user_login(self, request, *args, **kwargs):
        # 可以在此完成登录的逻辑
        request_data = request.data
        res = TUser.objects.filter(username=request_data.get("username"), password=request_data.get("password"))
        if res:
            return Response("登录成功")
        print(request_data)
        return Response("登录失败,用户名或密码错误")

    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)


class UserREGViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = TUser.objects.all()
    serializer_class = UserModelSerializer

    def user_register(self, request, *args, **kwargs):
        # 可以在此完成登录的逻辑
        request_data = request.data
        res = TUser.objects.filter(username=request_data.get("username"))
        if res:
            return Response("注册失败,用户名已存在")
        else:
            self.create(request, *args, **kwargs)
        print(request_data)
        return Response("注册成功")

    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)


class UserAPIView(APIView):
    # authentication_classes = [MyAuth]
    # permission_classes = [MyPermission]

    throttle_classes = [SendMessageRate]

    def get(self, request, *args, **kwargs):
        print("读请求")
        return Response("读请求")

    def post(self, request, *args, **kwargs):
        print("写请求")
        return Response("写请求")