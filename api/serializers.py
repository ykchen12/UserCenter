from rest_framework import serializers
from api.models import User, Dept


class UserSerializers(serializers.ModelSerializer):
    part_name = serializers.SerializerMethodField()

    class Meta:
        model = User  # 定义关联的Model
        fields = ('id', 'account', 'name', 'password', 'phone', 'email', 'dept', 'part_name')  # 指定返回的fields

    @staticmethod
    def get_part_name(obj):
        return obj.dept.name


class DeptSerializers(serializers.ModelSerializer):
    children_name = serializers.SerializerMethodField()

    class Meta:
        model = Dept
        fields = ('id', 'num', 'name', 'children', 'children_name')

    @staticmethod
    def get_children_name(obj):
        dist = []
        for i in obj.children.all():
            dist.append({'id': i.num, 'name': i.name})
        return dist
