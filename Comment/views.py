from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from . import models
import datetime
from django.http import HttpResponse, JsonResponse
from .models import Floor, Point, Article, WelcomeImage
from django.views import generic
import qrcode
from io import BytesIO

PREFIX_MEDIA = 'media/'
FLOORS_URL = 'Comment:floors'
POINTS_URL = 'Comment:points'
ARTICLES_URL = 'Comment:articles'
WCIMAGES_URL = 'Comment:welcomeImages'


def response(code: int, data):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def index_get(request):
    if request.GET.get('type') == 'get_comment':
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
        cnt = int(models.Comment.objects.count())
        code = 200
        if cnt < start:
            return response(202, "No Comment")
        elif cnt <= end:
            code = 202
            end = cnt
        return response(code, [
            {
                'time': each.time,
                'name': each.name,
                'text': each.text,
                'email': each.email
            }
            for each in models.Comment.objects.all().order_by('-time')[int(start): int(end)]
        ])

    elif request.GET.get('type') == "get_reply":
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
        father_name = request.GET.get('father_name')
        father_time = request.GET.get('father_time')
        conditions = {'father_name': father_name, 'father_time': father_time}
        results = models.Reply.objects.filter(**conditions)
        cnt = int(results.count())
        code = 200
        if cnt < start:
            return response(202, "No Reply")
        elif cnt <= end:
            code = 202
            end = cnt
        return response(code, [
            {
                'admin': each.admin,
                'time': each.time,
                'name': each.name,
                'text': each.text,
                'email': each.email,
            }
            for each in results.order_by('-time')[int(start): int(end)]
        ])

    elif request.GET.get('type') == "admin_reply":
        father_name = request.GET.get('father_name')
        conditions = {'father_name': father_name, 'admin': "1"}
        results = models.Reply.objects.filter(**conditions)
        cnt = int(results.count())
        if cnt == 0:
            return response(202, "No Admin Reply")
        else:
            return response(200, [
                {
                    'time': each.time,
                    'name': each.name,
                    'text': each.text,
                    'email': each.email,
                    'father_text': each.father_text,
                }
                for each in results.order_by('-time')
            ])


def index_post(request):
    if request.POST.get('type') == 'delete_comment':
        name = request.POST.get('name')
        text = request.POST.get('text')
        time = request.POST.get('time')
        conditions = {'name': name, 'text': text}
        conditions2 = {'father_name': name, 'father_time': time}
        result = models.Comment.objects.filter(**conditions)
        result2 = models.Reply.objects.filter(**conditions2)
        if int(result.count()) > 0:
            result.delete()
            if int(result2.count()) > 0:
                result2.delete()
            return HttpResponse("OK")
        else:
            return HttpResponse("No Such Comment(s)")

    elif request.POST.get('type') == 'delete_reply':
        name = request.POST.get('name')
        text = request.POST.get('text')
        conditions = {'name': name, 'text': text}
        result = models.Reply.objects.filter(**conditions)
        if int(result.count()) > 0:
            result.delete()
            return HttpResponse("OK")
        else:
            return HttpResponse("No Such Reply(s)")


def index(request):
    if request.method == 'GET':
        return index_get(request)

    elif request.method == 'POST':
        return index_post(request)


def create(request):
    return render(request, 'Comment/comments.html')


def save(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'create_comment':
            name = request.POST.get("name")
            email = request.POST.get("email")
            text = request.POST.get("text")
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            comment = models.Comment(name=name, email=email, text=text, time=time)
            if comment:
                comment.save()
                return HttpResponse("Ok")
            else:
                return HttpResponse("Failed")

        elif request.POST.get('type') == 'create_reply':
            name = request.POST.get("name")
            email = request.POST.get("email")
            text = request.POST.get("text")
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            father_name = request.POST.get("father_name")
            father_time = request.POST.get("father_time")
            father_text = request.POST.get("father_text")
            admin = request.POST.get("admin")
            reply = models.Reply(name=name, email=email, text=text, time=time, father_name=father_name,
                                 father_time=father_time, father_text=father_text, admin=admin)
            if reply:
                reply.save()
                return HttpResponse("OK")
            else:
                return HttpResponse("Failed")


def point(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'get_axis':
            lib = request.GET.get('library')
            num = request.GET.get('floor')
            conditions = {'library': lib, 'floor': num}
            return response(200, [
                {
                    'pos': each.position,
                    'x': each.x,
                    'y': each.y,
                    'order': each.order,
                }
                for each in models.Point.objects.filter(**conditions)
            ])

        elif request.GET.get('type') == 'get_info':
            pos = request.GET.get('pos')
            result = models.Point.objects.get(position=pos)
            return response(200, {
                'describe': result.describe,
                'floor': result.floor,
                'image': PREFIX_MEDIA + str(result.image),
                'video': PREFIX_MEDIA + str(result.video)
            })


def floor(request):
    if request.method == 'GET' and request.GET.get('type') == 'get_floor':
        lib = request.GET.get('library')
        num = request.GET.get('floor')
        conditions = {'library': lib, 'floor': num}
        result = models.Floor.objects.get(**conditions)
        return response(200, {
            'image': PREFIX_MEDIA + str(result.image),
            'full': PREFIX_MEDIA + str(result.panorama)
        })


def service(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'get_title':
            start = int(request.GET.get('start'))
            end = int(request.GET.get('end'))
            cnt = int(models.Article.objects.count())
            code = 200
            if cnt < start:
                return response(202, "No Article")
            elif cnt <= end:
                code = 202
                end = cnt
            return response(code, [
                each.title for each in models.Article.objects.all()[int(start): int(end)]
            ])

        elif request.GET.get('type') == 'get_url':
            _title = request.GET.get('title')
            result = models.Article.objects.get(title=_title)

            return response(200, result.url)


def welcome(request):
    if request.method == 'GET' and request.GET.get('type') == 'get_welcome':
        cnt = int(models.WelcomeImage.objects.count())
        if cnt > 0:
            result = models.WelcomeImage.objects.order_by('?').first()
            return response(200, [
                {
                    'image': PREFIX_MEDIA + str(result.image)
                }
            ])
        else:
            return response(202, "No Images")


def grade(request):
    if request.method == 'POST' and request.POST.get('type') == 'new_grade':
        star = request.POST.get('star')
        result = models.Grade.objects.filter(grade=star)
        if result.count() == 0:
            record = models.Grade(grade=star, sum=1)
            if record:
                record.save()
                return HttpResponse("OK")
            else:
                return HttpResponse("Failed")
        else:
            record = models.Grade.objects.get(grade=star)
            num = record.sum
            record.sum = num + 1
            record.save()
            return HttpResponse("OK")

    elif request.method == 'GET' and request.GET.get('type') == "get_grade":
        return response(200, [
            {
                'grade': each.grade,
                'sum': each.sum
            }
            for each in models.Grade.objects.all()
        ])


def visit(request):
    if request.method == 'POST' and request.POST.get('type') == 'new_visit':
        pos = request.POST.get('position')
        result = models.Visit.objects.filter(position=pos)
        if result.count() == 0:
            record = models.Visit(position=pos, sum=1)
            if record:
                record.save()
                return HttpResponse("OK")
            else:
                return HttpResponse("Failed")
        else:
            record = models.Visit.objects.get(position=pos)
            num = record.sum
            record.sum = num + 1
            record.save()
            return HttpResponse("OK")

    elif request.method == 'GET' and request.GET.get('type') == 'get_visit':
        pos = request.GET.get('position')
        result = models.Visit.objects.filter(position=pos)
        if result.count() == 0:
            return response(202, 0)
        else:
            record = models.Visit.objects.get(position=pos)
            return response(200, record.sum)


def manage(request):
    user = request.user
    num_floors = Floor.objects.all().count()
    num_points = Point.objects.all().count()
    num_articles = Article.objects.all().count()
    num_welcomeimages = WelcomeImage.objects.all().count()
    return render(request, 'manage.html', context={'user': user, 'num_floors': num_floors,
                                                     'num_points': num_points, 'num_articles': num_articles,
                                                     'num_welcomeimages': num_welcomeimages})


def permission_denied(request):
    return render(request, 'permission_denied.html')


def qr_code(request):
    if request.method == 'GET':
        pos = request.GET.get('position')
        library = request.GET.get('library')
        floor = request.GET.get('floor')
        describe = request.GET.get('describe')
        message = """
        #位置：%s\n
        #所在图书馆：%s\n
        #楼层：%s层\n
        #描述信息：%s\n
        #更多详细内容请见APP！！！""" % (pos, library, floor, describe)
        img = qrcode.make(message)
        buf = BytesIO()
        img.save(buf)
        image_stream = buf.getvalue()
        return HttpResponse(image_stream, content_type="image/png")


class FloorListView(generic.ListView):
    model = Floor
    template_name = 'floor_list.html'


class FloorDetailView(generic.DeleteView):
    model = Floor
    template_name = 'floor_detail.html'


class FloorCreateView(generic.CreateView):
    model = Floor
    fields = '__all__'
    template_name = 'floor_form.html'
    success_url = reverse_lazy(FLOORS_URL)


class FloorUpdateView(generic.UpdateView):
    model = Floor
    fields = '__all__'
    template_name = 'floor_form.html'
    success_url = reverse_lazy(FLOORS_URL)


class FloorDeleteView(generic.DeleteView):
    model = Floor
    success_url = reverse_lazy(FLOORS_URL)
    template_name = 'floor_confirm_delete.html'


class PointListView(generic.ListView):
    model = Point
    template_name = 'point_list.html'


class PointDetailView(generic.DetailView):
    model = Point
    template_name = 'point_detail.html'


class PointCreateView(generic.CreateView):
    model = Point
    fields = '__all__'
    template_name = 'point_form.html'
    success_url = reverse_lazy(POINTS_URL)


class PointUpdateView(generic.UpdateView):
    model = Point
    fields = '__all__'
    template_name = 'point_form.html'
    success_url = reverse_lazy(POINTS_URL)


class PointDeleteView(generic.DeleteView):
    model = Point
    success_url = reverse_lazy(POINTS_URL)
    template_name = 'point_confirm_delete.html'


class ArticleListView(generic.ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'


class ArticleCreateView(generic.CreateView):
    model = Article
    fields = '__all__'
    template_name = 'article_form.html'
    success_url = reverse_lazy(ARTICLES_URL)


class ArticleUpdateView(generic.UpdateView):
    model = Article
    fields = '__all__'
    template_name = 'article_form.html'
    success_url = reverse_lazy(ARTICLES_URL)


class ArticleDeleteView(generic.DeleteView):
    model = Article
    success_url = reverse_lazy(ARTICLES_URL)
    template_name = 'article_confirm_delete.html'


class WelcomeImageListView(generic.ListView):
    model = WelcomeImage
    template_name = 'welcomeImage_list.html'


class WelcomeImageDetailView(generic.DetailView):
    model = WelcomeImage
    template_name = 'welcomeImage_detail.html'


class WelcomeImageCreateView(generic.CreateView):
    model = WelcomeImage
    fields = '__all__'
    template_name = 'welcomeImage_form.html'
    success_url = reverse_lazy(WCIMAGES_URL)


class WelcomeImageUpdateView(generic.UpdateView):
    model = WelcomeImage
    fields = '__all__'
    template_name = 'welcomeImage_form.html'
    success_url = reverse_lazy(WCIMAGES_URL)


class WelcomeImageDeleteView(generic.DeleteView):
    model = WelcomeImage
    success_url = reverse_lazy(WCIMAGES_URL)
    template_name = 'welcomeImage_confirm_delete.html'
