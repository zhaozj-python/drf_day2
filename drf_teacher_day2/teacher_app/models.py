from django.db import models


# Create your models here.
class Teacher(models.Model):
    gender_choices = (
        (0, "男"),
        (1, "女"),
        (2, "秀吉"),
    )

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    phone = models.CharField(max_length=11, null=True, blank=True)
    pic = models.ImageField(upload_to="pic/", default="pic/1.jpg")
    classes = models.CharField(max_length=10, default="2006")

    class Meta:
        db_table = "bz_teacher"
        verbose_name = "老师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
