from rest_framework.response import Response

from rest_framework.views import APIView
# Create your views here.
from teacher_app.models import Teacher
from teacher_app.serializers import TeacherSerializer, TeacherDeSerializer


class TeacherAPIView(APIView):

    def get(self, request, *args, **kwargs):
        teacher_id = kwargs.get("id")
        if teacher_id:
            teacher_obj = Teacher.objects.get(pk=teacher_id)
            choose_teacher = TeacherSerializer(teacher_obj).data
            return Response({
                "status": 200,
                "message": "查询单个教师成功",
                "results": choose_teacher
            })
        else:
            all_the_teachers = Teacher.objects.all()
            all_teachers = TeacherSerializer(all_the_teachers, many=True).data
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
        print(post_serializer)
        if post_serializer.is_valid():
            add_teacher = post_serializer.save()
            return Response({
                "status": 200,
                "message": "教师添加成功",
                "results": TeacherSerializer(add_teacher).data
            })
        else:
            return Response({
                "status": 400,
                "message": "教师添加失败",
                # 保存失败的信息会包含在 .errors中
                "results": post_serializer.errors
            })
