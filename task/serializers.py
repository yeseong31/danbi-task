from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at']
