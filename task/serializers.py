from rest_framework import serializers

from account.serializers import TeamSerializer, UserProfileSerializer
from task.models import Task, SubTask


class SubTaskDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'team', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)
        

class SubTaskCreateSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    
    class Meta:
        model = SubTask
        fields = ('team', )
        

class TaskListSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True, many=True)
    create_user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)


class TaskDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    create_user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)
    
    @classmethod
    def setup_preloading(cls, queryset):
        return queryset.select_related('team')
    
    
class TaskCreateSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    create_user = UserProfileSerializer()
    
    class Meta:
        model = Task
        fields = ('team', 'title', 'content', 'create_user')
        
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    create_user = UserProfileSerializer()
    
    class Meta:
        model = Task
        fields = ('team', 'title', 'content', 'create_user')
