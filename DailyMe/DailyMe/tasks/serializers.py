from rest_framework import serializers, validators, exceptions

from .models import Task, TaskToDo
from .services.date import get_date_edges
from loguru import logger


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(write_only=True, default=serializers.CurrentUserDefault())

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super().run_validators(value)

    def create(self, validated_data):
        instance, _ = Task.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Task
        fields = '__all__'


class ParseCategory(serializers.Field):
    def to_internal_value(self, data):
        try:
            return get_date_edges(data)
        except ValueError:
            raise serializers.ValidationError('Wrong category')


class ToDoSerializer(serializers.ModelSerializer):
    category = ParseCategory(write_only=True)
    
    def run_validation(self, data):
        data = {**super().run_validation(data)}
        if data['task'].owner != self.context['request'].user:
            raise exceptions.PermissionDenied()

        if (dates := data.pop('category')) is not None:
            data['start_date'] = dates[0].to_datetime_string()
            data['end_date'] =dates[1].to_datetime_string()
        return data

    class Meta:
        model = TaskToDo
        fields = "__all__"
        read_only_fields = ('start_date', 'end_date')
