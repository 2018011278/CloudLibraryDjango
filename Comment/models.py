from django.db import models
from django.urls import reverse
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name='用户名', null=False, blank=True, default="")
    email = models.EmailField(verbose_name='邮箱', null=False, blank=True, default="")
    text = models.TextField(verbose_name='留言内容', null=False, blank=True, default="")
    time = models.DateTimeField(default=timezone.now(), verbose_name='创建时间', null=False, blank=False)


class Reply(models.Model):
    name = models.CharField(max_length=100, verbose_name='用户名', null=False, blank=True, default="")
    email = models.EmailField(verbose_name='邮箱', null=False, blank=True, default="")
    text = models.TextField(verbose_name='留言内容', null=False, blank=True, default="")
    time = models.DateTimeField(default=timezone.now(), verbose_name='创建时间', null=False, blank=False)
    father_name = models.CharField(max_length=100, verbose_name='父评论名', null=False, blank=True, default="")
    father_time = models.CharField(max_length=100, verbose_name='父评论时间', null=False, blank=False)
    father_text = models.TextField(verbose_name='回复内容', null=False, blank=True, default="")
    admin = models.CharField(max_length=1, verbose_name='管理员', null=False, blank=False, default="0")


class Grade(models.Model):
    grade = models.CharField(max_length=5, verbose_name='分数', null=False, blank=False, default="")
    sum = models.IntegerField(verbose_name='计数', null=False, blank=False, default=0)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='文章标题', null=False, blank=True, default="")
    url = models.CharField(max_length=400, verbose_name='文章网址', null=False, blank=False)

    def get_absolute_url(self):
        return reverse('Comment:article-detail', args=[str(self.id)])


class WelcomeImage(models.Model):
    image = models.ImageField(upload_to='image/welcome', null=True, blank=True, verbose_name="欢迎图片")

    def get_absolute_url(self):
        return reverse('Comment:welcomeImage-detail', args=[str(self.id)])


class Visit(models.Model):
    position = models.CharField(max_length=200, verbose_name='位置', null=False, blank=False)
    sum = models.IntegerField(verbose_name='访问量', null=False, blank=False, default=0)


class Point(models.Model):
    position = models.CharField(max_length=200, verbose_name='位置', null=False, blank=False)
    library = models.CharField(max_length=50, verbose_name='馆属', null=False, blank=False)
    floor = models.CharField(max_length=50, verbose_name='层', null=False, blank=False, default='0')
    x = models.IntegerField(verbose_name='x坐标', null=False, blank=False, default=-1)
    y = models.IntegerField(verbose_name='y坐标', null=False, blank=False, default=-1)
    describe = models.CharField(verbose_name='描述', max_length=512)
    image = models.ImageField(upload_to='image/point', null=True, blank=True, verbose_name="描述图片")
    video = models.FileField(upload_to='video/', null=True, blank=True, verbose_name="描述视频")
    order = models.IntegerField(verbose_name='导览顺序', null=False, blank=False, default=0)

    def get_absolute_url(self):
        return reverse('Comment:point-detail', args=[str(self.id)])

    
class Floor(models.Model):
    library = models.CharField(max_length=50, verbose_name='馆属', null=False, blank=False)
    floor = models.CharField(max_length=50, verbose_name='层', null=False, blank=False, default='0')
    image = models.ImageField(upload_to='image/floor', null=True, blank=True, verbose_name="描述图片")
    panorama = models.ImageField(upload_to='image/floor', null=True, blank=True, verbose_name="全景图片")

    def get_absolute_url(self):
        return reverse('Comment:floor-detail', args=[str(self.id)])
