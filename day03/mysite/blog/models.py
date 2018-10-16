from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

class UserManager(models.Manager):

    def add_user(self, username, password, age, email):
        return self.create(username=username, password=password, age=age, email=email)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名称")
    password = models.CharField(max_length=255, verbose_name="用户密码")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    nickname = models.CharField(max_length=255, null=True, blank=True, verbose_name="用户昵称")
    birthday = models.DateTimeField(default=datetime.now(), verbose_name="用户生日")
    email = models.EmailField(max_length=255, verbose_name="用户邮箱")
    # 默认是0 表示男生， 1表示女生
    gender = models.BooleanField(default=0)
    header = models.ImageField(upload_to='static/img/headers/', default="static/img/default.png", verbose_name="用户头像")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nickname

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="文章标题")
    content = UEditorField()
    publishTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)

    # 外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publishTime']

    # um = UserManager()

    # class Meta:
    #     db_table = "t_user"

    # @classmethod
    # def create_user(cls, username, password, age, email):
    #     user = cls(username=username, password=password, age=age, email=email)
    #     return user

    def __str__(self):
        return self.username


