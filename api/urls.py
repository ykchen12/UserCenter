from django.conf.urls import url
from django.contrib import admin
from api import views
from api.views import UserViewSet, DepartViewSet, UserAll, UserOne, AllDepart
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'department', DepartViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include(router.urls)),
    url(r'login$', views.AuthView.as_view()),
    url(r'^userlist/$', UserAll.as_view()),
    path(r'userlist/<str:id>', UserOne.as_view()),
    url(r'^department/$', AllDepart.as_view()),

]
