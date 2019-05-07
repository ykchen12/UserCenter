from rest_framework import serializers
from api.models import User, Department


class UserSerializers(serializers.ModelSerializer):
    part_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'account', 'name', 'password', 'email', 'department', 'part_name')

    def get_part_name(self, obj):
        return obj.department.name


class DepartSerializers(serializers.ModelSerializer):
    children_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'num', 'name', 'children', 'children_name')

    def get_children_name(self, obj):
        DIST = []
        for i in obj.children.all():
            DIST.append({'id': i.num, 'name': i.name})
        return DIST
