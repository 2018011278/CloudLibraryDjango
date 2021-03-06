# Generated by Django 3.1.2 on 2020-11-06 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200, verbose_name='文章标题')),
                ('url', models.CharField(max_length=400, verbose_name='文章网址')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, verbose_name='用户名')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='邮箱')),
                ('text', models.TextField(blank=True, default='', verbose_name='留言内容')),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 11, 6, 12, 24, 33, 83570), verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library', models.CharField(max_length=50, verbose_name='馆属')),
                ('floor', models.CharField(default='0', max_length=50, verbose_name='层')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/floor', verbose_name='描述图片')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=200, verbose_name='位置')),
                ('library', models.CharField(max_length=50, verbose_name='馆属')),
                ('floor', models.CharField(default='0', max_length=50, verbose_name='层')),
                ('x', models.IntegerField(default=-1, verbose_name='x坐标')),
                ('y', models.IntegerField(default=-1, verbose_name='y坐标')),
                ('describe', models.CharField(max_length=512, verbose_name='描述')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/point', verbose_name='描述图片')),
                ('video', models.FileField(blank=True, null=True, upload_to='video/', verbose_name='描述视频')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, verbose_name='用户名')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='邮箱')),
                ('text', models.TextField(blank=True, default='', verbose_name='留言内容')),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 11, 6, 12, 24, 33, 93565), verbose_name='创建时间')),
                ('father_name', models.CharField(blank=True, default='', max_length=100, verbose_name='父评论名')),
                ('father_time', models.CharField(max_length=100, verbose_name='父评论时间')),
                ('admin', models.CharField(default='0', max_length=1, verbose_name='管理员')),
            ],
        ),
    ]
