from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task
from django.utils import timezone

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSummarySerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'is_completed']
    def validate_due_date(self, value):
        user = self.context['request'].user
        if user.is_staff:
            return value # Admins can do whatever they want
        # Check if the date is in the past
        if value < timezone.now().date():
            raise serializers.ValidationError("The due date cannot be in the past!")
        return value
    def validate(self, data):
    # Check if 'title' AND 'description' are both in the current request (data)
    # If they aren't both there (like in a PATCH), we skip this specific check
        if 'title' in data and 'description' in data:
             title = data.get('title', '')
             description = data.get('description', '')

             if title.lower() in description.lower():
                raise serializers.ValidationError({
                    "description": "Description should provide new info, not just repeat the title."
                })
    
        return data

class EmployeeTaskUpdateSerializer(serializers.ModelSerializer):
    # We mark these as read_only so the API ignores them if an employee tries to change them
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    assigned_to = UserSummarySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'is_completed']

