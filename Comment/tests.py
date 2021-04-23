from django.test import TestCase, RequestFactory
from django.urls.resolvers import RegexPattern
from .models import Floor, Point, Article, WelcomeImage, Comment, Reply, Visit
from .views import FloorListView, FloorCreateView, FloorDetailView, FloorUpdateView, FloorDeleteView
from .views import PointListView, PointCreateView, PointDetailView, PointUpdateView, PointDeleteView
from .views import ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from .views import WelcomeImageListView, WelcomeImageCreateView, WelcomeImageDetailView, \
    WelcomeImageUpdateView, \
    WelcomeImageDeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import resolve, reverse
import pytest


# Create your tests here.

class FloorListViewTest(TestCase):
    def test_floor_list(self):
        resolver = resolve('/manage/floors/')
        self.assertEqual(resolver.func.__name__, FloorListView.as_view().__name__)


class FloorCreateViewTest(TestCase):
    def test_floor_create(self):
        resolver = resolve('/manage/floor/create/')
        self.assertEqual(resolver.func.__name__, FloorCreateView.as_view().__name__)


class FloorDetailViewTest(TestCase):
    def setUp(self):
        self.floor = Floor.objects.create(
            library='北馆',
            floor='1',
            image='x'
        )

    def test_floor_detail_not_staff(self):
        response = self.client.get(reverse('Comment:floor-detail', kwargs={'pk': self.floor.pk}))
        # print(response)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/manage/permission_denied/', fetch_redirect_response=False)


class FloorUpdateViewTest(TestCase):
    def setUp(self):
        self.floor = Floor.objects.create(
            library='北馆',
            floor='1',
            image='x'
        )

    def test_floor_update_not_staff(self):
        response = self.client.get(reverse('Comment:floor_update', kwargs={'pk': self.floor.pk}))

        self.assertEqual(response.status_code, 302)


class FloorDeleteViewTest(TestCase):
    def setUp(self):
        self.floor = Floor.objects.create(
            library='北馆',
            floor='1',
            image='x'
        )

    def test_floor_delete_not_staff(self):
        response = self.client.get(reverse('Comment:floor_delete', kwargs={'pk': self.floor.pk}))

        self.assertEqual(response.status_code, 302)


class PointListViewTest(TestCase):
    def test_point_list(self):
        resolver = resolve('/manage/points/')
        self.assertEqual(resolver.func.__name__, PointListView.as_view().__name__)


class PointCreateViewTest(TestCase):
    def test_point_create(self):
        resolver = resolve('/manage/point/create/')
        self.assertEqual(resolver.func.__name__, PointCreateView.as_view().__name__)


class PointDetailViewTest(TestCase):
    def setUp(self):
        self.point = Point.objects.create(
            position='1',
            library='1',
            floor='1',
            x='1',
            y='1',
            describe='1',
            image='1',
            video='1'
        )

    def test_point_detail_not_staff(self):
        response = self.client.get(reverse('Comment:point-detail', kwargs={'pk': self.point.pk}))

        self.assertEqual(response.status_code, 302)


class PointUpdateViewTest(TestCase):
    def setUp(self):
        self.point = Point.objects.create(
            position='1',
            library='1',
            floor='1',
            x='1',
            y='1',
            describe='1',
            image='1',
            video='1'
        )

    def test_point_update_not_staff(self):
        response = self.client.get(reverse('Comment:point_update', kwargs={'pk': self.point.pk}))

        self.assertEqual(response.status_code, 302)


class PointDeleteViewTest(TestCase):
    def setUp(self):
        self.point = Point.objects.create(
            position='1',
            library='1',
            floor='1',
            x='1',
            y='1',
            describe='1',
            image='1',
            video='1'
        )

    def test_point_delete_not_staff(self):
        response = self.client.get(reverse('Comment:point_delete', kwargs={'pk': self.point.pk}))

        self.assertEqual(response.status_code, 302)


@pytest.mark.django_db
def test_index_view(client):
    url = reverse('Comment:index')
    data = {
        'type': 'get_comment',
        'start': 1,
        'end': 3,
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    Comment.objects.create()
    response = client.get(url, data=data)
    assert response.status_code == 202
    Comment.objects.create()
    Comment.objects.create()
    Comment.objects.create()
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'get_reply',
        'start': 1,
        'end': 2,
        'father_name': 'father_name',
        'father_time': 'father_time',
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    Reply.objects.create(father_name='father_name', father_time='father_time')
    response = client.get(url, data=data)
    assert response.status_code == 202
    Reply.objects.create(father_name='father_name', father_time='father_time')
    Reply.objects.create(father_name='father_name', father_time='father_time')
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'admin_reply',
        'father_name': 'father_name',
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    Reply.objects.create(father_name='father_name', admin=1)
    response = client.get(url, data=data)
    assert response.status_code == 200
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'delete_comment',
        'name': 'name_delete',
        'text': 'text_delete',
        'time': 'time_delete'
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    Comment.objects.create(name='name_delete', text='text_delete')
    Reply.objects.create(father_name='name_delete', father_time='time_delete')
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'delete_reply',
        'name': 'name_delete2',
        'text': 'text_delete2',
        'time': 'time_delete2'
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    Reply.objects.create(name='name_delete2', text='text_delete2')
    response = client.post(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_view(client):
    url = reverse('Comment:create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    '_type, name, email, text, admin, status_code', [
        ('create_comment', '', '', '', '', 200),
        ('create_comment', 'name', 'email.email.com', 'text', '', 200),
        ('create_reply', 'name', 'email@email.com', 'text', '', 200)
    ]
)
def test_save_view(_type, name, email, text, status_code, admin, client):
    url = reverse('Comment:save')
    data = {
        'type': _type,
        'name': name,
        'email': email,
        'text': text,
        'father_name': '',
        'father_time': '',
        'father_text': '',
        'admin': admin,
    }
    response = client.post(url, data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_service_view(client):
    url = reverse('Comment:service')
    data = {
        'type': 'get_title',
        'start': 1,
        'end': 2,
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    Article.objects.create()
    response = client.get(url, data=data)
    assert response.status_code == 202
    Article.objects.create()
    Article.objects.create(title='title')
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'get_url',
        'title': 'title',
    }
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_welcome_view(client):
    url = reverse('Comment:welcome')
    data = {
        'type': 'get_welcome',
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    WelcomeImage.objects.create()
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_point_view(client):
    url = reverse('Comment:point')
    data = {
        'type': 'get_axis',
        'library': '1',
        'floor': '2',
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'get_info',
        'pos': '3'
    }
    Point.objects.create(position='3')
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_floor_view(client):
    url = reverse('Comment:floor')
    data = {
        'type': 'get_floor',
        'library': '1',
        'floor': '2',
    }
    Floor.objects.create(library='1', floor='2')
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_grade_view(client):
    url = reverse('Comment:grade')
    data = {
        'type': 'new_grade',
        'star': 1,
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'get_grade'
    }
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_visit_view(client):
    url = reverse('Comment:visit')
    data = {
        'type': 'get_visit',
        'position': '1',
    }
    response = client.get(url, data=data)
    assert response.status_code == 202
    data = {
        'type': 'new_visit',
        'position': '1',

    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        'type': 'get_visit',
        'position': '1',
    }
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_manage_view(client):
    url = reverse('Comment:manage')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_denied_view(client):
    url = reverse('Comment:permission_denied')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_qrcode_view(client):
    url = reverse('Comment:qr')
    response = client.get(url)
    assert response.status_code == 200
