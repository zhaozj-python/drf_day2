from django.conf import settings
from rest_framework import serializers
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

    def create(self, validated_data):
        # print(self)
        # print(validated_data)
        return Teacher.objects.create(**validated_data)
