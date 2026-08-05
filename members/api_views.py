from rest_framework import generics, permissions, filters
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # Must be logged in

    def get_queryset(self):
        # The 'request' object contains the user who sent the Token
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        # Filter the database: Only return tasks where assigned_to matches this user
        return Task.objects.filter(assigned_to=user)
    # 1. Add the filter "Engines"
    filter_backends = [
        DjangoFilterBackend,    # For exact matches (e.g., is_completed=True)
        filters.SearchFilter,   # For text search (e.g., search=website)
        filters.OrderingFilter  # For sorting (e.g., ordering=due_date)
    ]

    # 2. Define which fields can be filtered/searched
    filterset_fields = ['is_completed', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'title']
        


class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # If the user is an admin/staff, give them the full power serializer
        if self.request.user.is_staff:
            return TaskSerializer
        
        # If they are just an employee, give them the restricted serializer
        return EmployeeTaskUpdateSerializer

class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # If the user is an admin/staff, give them the full power serializer
        if self.request.user.is_staff:
            return TaskSerializer
        
        # If they are just an employee, give them the restricted serializer
        return EmployeeTaskUpdateSerializer