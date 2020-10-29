from rest_framework.response import Response

from rest_framework.views import APIView
# Create your views here.
from teacher_app.models import Teacher
from teacher_app.serializers import TeacherSerializer, TeacherDeSerializer, TeacherModelSerializer


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


