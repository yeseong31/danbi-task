from rest_framework import serializers

from task.models import Task, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'username', 'team',)


class TaskSerializer(serializers.ModelSerializer):
    subtask = SubTaskSerializer(read_only=True)  # nested serializer

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('create_user', 'team', 'title', 'content',)
