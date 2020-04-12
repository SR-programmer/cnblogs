from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):
    phone = models.BigIntegerField(null=True,blank=True)  # blank是用来告诉admin后台 该字段可以不填
    # avatar存的是用户头像文件路径 用户上传的头像会自动保存到avatar文件夹下
    avatar = models.FileField(upload_to='avatar/',default='avatar/default.jpg')
    create_time = models.DateField(auto_now_add=True)

    blog = models.OneToOneField(to='Blog',null=True)

    class Meta:
        verbose_name_plural = '用户表'
        # verbose_name =  '用户表'

    def __str__(self):
        return self.username


class Blog(models.Model):
    site_title = models.CharField(max_length=32)
    site_name = models.CharField(max_length=32)
    site_theme = models.CharField(max_length=255)


    def __str__(self):
        return self.site_name

class Category(models.Model):
    name = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog')
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog')
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    content = models.TextField()  # 存大段文本
    create_time = models.DateField(auto_now_add=True)

    # 数据库优化字段
    comment_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)

    # 外键字段
    blog = models.ForeignKey(to='Blog',null=True)
    category = models.ForeignKey(to='Category',null=True)
    tag = models.ManyToManyField(to='Tag',through='Article2Tag',through_fields=('article','tag'))

    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')



class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField()  # 传布尔值  存0/1


class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(max_length=255)
    create_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(to='self',null=True)



