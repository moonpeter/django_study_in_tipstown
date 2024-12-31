from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


# noinspection PyAbstractClass
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

    # https://gaussian37.github.io/python-rest-nested-serializer/
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['created_by'] = UserSerializer(instance.created_by).data
        return res
