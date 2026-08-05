from django.contrib import admin
from .models import Task

class MemberAdmin(admin.ModelAdmin):
    # Use fields that actually exist in your Task model
    list_display = ('title', 'assigned_to', 'due_date', 'is_completed')
    list_filter = ('is_completed', 'priority')
    search_fields = ('title', 'description')

admin.site.register(Task, MemberAdmin)