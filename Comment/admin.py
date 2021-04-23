from django.contrib import admin
from .models import Comment, Floor, Point, Reply, Article,\
    WelcomeImage, Grade, Visit

admin.site.register(Comment)
admin.site.register(Floor)
admin.site.register(Point)
admin.site.register(Reply)
admin.site.register(Article)
admin.site.register(WelcomeImage)
admin.site.register(Grade)
admin.site.register(Visit)
