from django.conf import settings
from rest_framework import serializers, exceptions
from teacher_app.models import Teacher


class TeacherSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.IntegerField()
    classes = serializers.CharField()
    phone = serializers.CharField()
    pic = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    def get_grade(self, obj):
        return "特级教师"

    def get_pic(self, obj):
        print(obj.pic)
        return "%s%s%s" % ("http://127.0.0.1:8000/", settings.MEDIA_URL, str(obj.pic))


class TeacherDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=10,
        min_length=2,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField()
    # classes = serializers.CharField()
    # gender = serializers.IntegerField()
    re_pwd = serializers.CharField()

    def validate(self, attrs):
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if pwd != re_pwd:
            raise exceptions.ValidationError("密码不一致")
        return attrs

    def create(self, validated_data):
        # print(self)
        # print(validated_data)
        return Teacher.objects.create(**validated_data)


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("username", "password", "gender", "classes", "phone", "grade", "pic_full")

        extra_kwargs = {
            "username": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "max_length": 10,
                "error_messages": {
                    "required": "用户名必须提供",
                    "min_length": "用户名不能少于两个字符",
                    "max_length": "用户名不能多于十个字符",
                }
            },
            # "re_pwd": {
            #     "write_only": True
            # },
            "password": {
                "write_only": True
            },
            "gender": {
                "read_only": True
            },
            "classes": {
                "read_only": True
            },
            "grade": {
                "read_only": True
            },
            "pic_full": {
                "read_only": True
            }

        }

        # def validate(self, attrs):
        #     pwd = attrs.get("password")
        #     re_pwd = attrs.pop("re_pwd")
        #     if pwd != re_pwd:
        #         raise exceptions.ValidationError("密码不一致")
        #     return attrs


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("username", "password")

        extra_kwargs = {
            "username": {
                "required": True,  # 必填字段
                "min_length": 2,  # 最小长度
                "max_length": 10,
                "error_messages": {
                    "required": "用户名必须提供",
                    "min_length": "用户名不能少于两个字符",
                    "max_length": "用户名不能多于十个字符",
                }
            },
            "password": {
                "write_only": True
            },
            # "re_pwd": {
            #     "write_only": True
            # },
        }

        # def validate(self, attrs):
        #     pwd = attrs.get("password")
        #     re_pwd = attrs.pop("re_pwd")
        #     if pwd != re_pwd:
        #         raise exceptions.ValidationError("密码不一致")
        #     return attrs
