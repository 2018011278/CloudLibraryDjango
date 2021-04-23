from django.conf.urls import url
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'Comment'
PERMISSION_DENIED = 'Comment:permission_denied'
urlpatterns = [
    url(r'^comment/index/$', views.index, name='index'),
    url(r'^comment/create/$', views.create, name='create'),
    url(r'^comment/save/$', views.save, name='save'),
    url(r'^detail/floor/$', views.floor, name='floor'),
    url(r'^detail/point/$', views.point, name='point'),
    url(r'^article/$', views.service, name='service'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^grade/$', views.grade, name='grade'),
    url(r'^visit/$', views.visit, name='visit'),
    url(r'^qr/$', views.qr_code, name='qr'),

    url(r'^manage/$', views.manage, name='manage'),
    path('manage/accounts/', include('django.contrib.auth.urls')),

    url(r'^manage/floors/$', views.FloorListView.as_view(), name='floors'),
    url(r'^manage/points/$', views.PointListView.as_view(), name='points'),
    url(r'^manage/articles/$', views.ArticleListView.as_view(), name='articles'),
    url(r'^manage/welcomeImages/$', views.WelcomeImageListView.as_view(), name='welcomeImages'),

    url(r'^manage/permission_denied$', views.permission_denied, name='permission_denied'),

    url(r'^manage/floor/(?P<pk>\d+)$', staff_member_required(views.FloorDetailView.as_view(),
                                                             login_url=reverse_lazy(PERMISSION_DENIED)
                                                             ), name='floor-detail'),
    url(r'^manage/floor/create/$', staff_member_required(views.FloorCreateView.as_view(),
                                                         login_url=reverse_lazy(PERMISSION_DENIED)
                                                         ), name='floor_create'),
    url(r'^manage/floor/(?P<pk>\d+)/update/$', staff_member_required(views.FloorUpdateView.as_view(),
                                                                     login_url=reverse_lazy(PERMISSION_DENIED)
                                                                     ), name='floor_update'),
    url(r'^manage/floor/(?P<pk>\d+)/delete/$', staff_member_required(views.FloorDeleteView.as_view(),
                                                                     login_url=reverse_lazy(PERMISSION_DENIED)
                                                                     ), name='floor_delete'),

    url(r'^manage/point/(?P<pk>\d+)$', staff_member_required(views.PointDetailView.as_view(),
                                                             login_url=reverse_lazy(PERMISSION_DENIED)
                                                             ), name='point-detail'),
    url(r'^manage/point/create/$', staff_member_required(views.PointCreateView.as_view(),
                                                         login_url=reverse_lazy(PERMISSION_DENIED)
                                                         ), name='point_create'),
    url(r'^manage/point/(?P<pk>\d+)/update/$', staff_member_required(views.PointUpdateView.as_view(),
                                                                     login_url=reverse_lazy(PERMISSION_DENIED)
                                                                     ), name='point_update'),
    url(r'^manage/point/(?P<pk>\d+)/delete/$', staff_member_required(views.PointDeleteView.as_view(),
                                                                     login_url=reverse_lazy(PERMISSION_DENIED)
                                                                     ), name='point_delete'),

    url(r'^manage/article/(?P<pk>\d+)$', staff_member_required(views.ArticleDetailView.as_view(),
                                                               login_url=reverse_lazy(PERMISSION_DENIED)
                                                               ), name='article-detail'),
    url(r'^manage/article/create/$', staff_member_required(views.ArticleCreateView.as_view(),
                                                           login_url=reverse_lazy(PERMISSION_DENIED)
                                                           ), name='article_create'),
    url(r'^manage/article/(?P<pk>\d+)/update/$', staff_member_required(views.ArticleUpdateView.as_view(),
                                                                       login_url=reverse_lazy(PERMISSION_DENIED)
                                                                       ), name='article_update'),
    url(r'^manage/article/(?P<pk>\d+)/delete/$', staff_member_required(views.ArticleDeleteView.as_view(),
                                                                       login_url=reverse_lazy(PERMISSION_DENIED)
                                                                       ), name='article_delete'),

    url(r'^manage/welcomeImage/(?P<pk>\d+)$', staff_member_required(views.WelcomeImageDetailView.as_view(),
                                                                    login_url=reverse_lazy(PERMISSION_DENIED)
                                                                    ), name='welcomeImage-detail'),
    url(r'^manage/welcomeImage/create/$', staff_member_required(views.WelcomeImageCreateView.as_view(),
                                                                login_url=reverse_lazy(PERMISSION_DENIED)
                                                                ), name='welcomeImage_create'),
    url(r'^manage/welcomeImage/(?P<pk>\d+)/update/$', staff_member_required(views.WelcomeImageUpdateView.as_view(),
                                                                            login_url=reverse_lazy(PERMISSION_DENIED)
                                                                            ), name='welcomeImage_update'),
    url(r'^manage/welcomeImage/(?P<pk>\d+)/delete/$', staff_member_required(views.WelcomeImageDeleteView.as_view(),
                                                                            login_url=reverse_lazy(PERMISSION_DENIED)
                                                                            ), name='welcomeImage_delete'),
]
