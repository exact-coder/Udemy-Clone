from rest_framework.serializers import ModelSerializer
from users.models import User
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=[
            'name'
        ]

class UserAuthSerializer(ModelSerializer):
    courses = serializers.ListField(source="get_all_courses")
    class Meta:
        model=User
        fields=[
            'id','name','courses','email'
        ]
