from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(write_only=True, default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        return TaskSerializer(instance).data

    class Meta:
        model = Task
        fields = '__all__'
