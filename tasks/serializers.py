from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import Task, Label

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'completion_status', 'owner', 'label']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id','name', 'owner']