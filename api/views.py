from rest_framework import viewsets
from api.models import Department, User
from api.serializers import UserSerializers, DepartSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from api import models
from api.cryp import decrypt_p
from rest_framework import exceptions
import hashlib
import time


class Authentication(BaseAuthentication):
    """
    认证类
    """

    def authenticate(self, request):
        token = request._request.GET.get("token")
        toke_obj = models.UserToken.objects.filter(token=token).first()
        if not toke_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (toke_obj.api, toke_obj)  # 这里返回值一次给request.api,request.auth

    def authenticate_header(self, val):
        pass


def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):
    """登陆认证"""

    def dispatch(self, request, *args, **kwargs):
        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse('get')

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': "登录成功"}
        try:
            account = request._request.POST.get("account")
            pwd = request._request.POST.get("password")
            obj = models.User.objects.get(account=account)
            # obj = models.User.objects.filter(account=account, password=pwd).first()
            if not obj or decrypt_p(obj.password) != pwd:
                ret['code'] = 403
                ret['msg'] = "用户名或密码错误"
            else:
                token = md5(account)
                models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
                ret['token'] = token
                ret['username'] = obj.name
                ret['account'] = obj.account

        except Exception as e:
            ret['code'] = 404
            ret['msg'] = "该用户未注册"

        return JsonResponse(ret)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DepartViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartSerializers


'''
class UserLogin():
    def get_obj(self, account):
        try:
            return User.objects.get(account=account)
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        account = request.POST.get('username')
        password = request.POST.get('password')
        api = self.get_obj(account)
        if api.password == password:
            usersar = UserSerializers(api)
            return Response(usersar.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
'''


def UserLogin(request):
    if request.method == 'POST':
        account = request.POST.get('username')
        password = request.POST.get('password')
        print(account, password)
        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            raise Http404
        if user.password == password:
            usersar = UserSerializers(user)
            return Response(usersar.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserOne(APIView):
    def get(self, request, id, format=None):
        try:
            user = Department.objects.get(num=str(id)).depart_name.all()
            serializer = UserSerializers(user, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAll(APIView):
    def get(self, request, format=None):
        department = User.objects.all()
        serializer = UserSerializers(department, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllDepart(APIView):
    def get(self, request, format=None):
        department = Department.objects.all()
        serializer = DepartSerializers(department, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)