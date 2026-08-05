from django.urls import path
from . import views
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token # Import the view
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [ 
       path('', views.login_user, name='login_user'),
       path('login/', views.log, name='log'),
       path('logout/', views.logout_user, name='logout'),
       path('admin-dash/', views.admin_dash, name='admin_dashboard'),
       path('employee-dash/', views.employee_dash, name='employee_dashboard'),
       path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
       path('signup/', views.signup_user, name='signup'),
       path('task/add/', views.add_task, name='add_task'),
       path('task/edit/<int:pk>/', views.edit_task, name='edit_task'),
       path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
       path('profile/edit/', views.edit_profile, name='edit_profile'),
       path('tasks/', api_views.TaskListCreateAPI.as_view(), name='task_api_list'),
       path('tasks/<int:pk>/', api_views.TaskDetailAPI.as_view(), name='task_detail'),
       path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
       # 1. The Raw Schema (The technical file behind the UI)
       path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
       # 2. Swagger UI (The Interactive "Try it out" interface)
       path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
       # 3. ReDoc (A cleaner, read-only interface)
       path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]