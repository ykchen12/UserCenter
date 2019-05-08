from django.conf.urls import url
from django.contrib import admin
from api import views
from api.views import UserViewSet, DeptViewSet, UserDetail, DeptList, UserList
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'dept', DeptViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include(router.urls)),
    url(r'login$', views.AuthView.as_view()),
    url(r'^userlist/$', UserList.as_view()),
    path(r'userlist/<str:id>', UserDetail.as_view()),
    url(r'^dept/$', DeptList.as_view()),

]
