from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date', 'priority']
        widgets = {
            # Adding Bootstrap classes to the auto-generated fields
            'assigned_to': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the dropdown to only show non-admin employees
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=False)