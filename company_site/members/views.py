from django.http import HttpResponse
from django.template import loader
from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_employee(user):
    # This ensures they are logged in but NOT an admin
    return user.is_authenticated and not user.is_staff

# The Admin Dashboard View
@login_required # This ensures only logged-in users can see this
@user_passes_test(is_admin)
def admin_dash(request):
    all_tasks = Task.objects.all() # Fetch every task in the DB
    all_tasks = Task.objects.all().order_by('-id')# '-id' puts newest at the top
    return render(request, 'admin_dashboard.html', {'tasks': all_tasks})
    # You can fetch admin-specific data here later


# The Employee Dashboard View
@login_required
@user_passes_test(is_employee, login_url='login_user')
def employee_dash(request):
    # Fetch tasks assigned to the CURRENT logged-in user
    user_tasks = Task.objects.filter(assigned_to=request.user, is_completed=False)
    # You can fetch employee-specific data (like their personal tasks) here
    return render(request, 'employee_dashboard.html', {
        'tasks': user_tasks
    })

def log(request):
    template = loader.get_template(log.html)
    return HttpResponse(template.render())

@ensure_csrf_cookie
def login_user(request):
    current_token = get_token(request)
    if request.method == "POST":
        # 1. Capture the data from the form
        un = request.POST.get('username')
        ps = request.POST.get('password')
        remember = request.POST.get('remember_me')

        # 2. Authenticate against the database
        user = authenticate(request, username=un, password=ps)

        

        if user is not None:
            print(f"DEBUG: Login Success for {un}!")
            login(request, user)

            if remember:
                # Set session to expire in 2 weeks (1209600 seconds)
                request.session.set_expiry(1209600)
            else:
                # Session expires when the browser is closed
                request.session.set_expiry(0)
            # 3. Role Detection Logic
            if user.is_staff: # Built-in Django way to check for Admin
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            print(f"DEBUG: Login FAILED for {un}")
            # If login fails, send an error message back
            return render(request, 'myloginpage.html', {'error': 'Invalid credentials', 'csrf_token': current_token})

    return render(request, 'myloginpage.html', {'csrf_token': current_token})

def complete_task(request, task_id):
    # Security: Ensure the task exists AND belongs to the logged-in user
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == "POST":
        task.is_completed = True
        task.save()
        
    return redirect('employee_dashboard')


def signup_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        uname = request.POST.get('username')
        psw = request.POST.get('password')
        role = request.POST.get('role') # 'admin' or 'employee'

        # Basic check to see if username is taken
        if User.objects.filter(username=uname).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        # Create the user
        user = User.objects.create_user(username=uname, email=email, password=psw)
        user.first_name = name
        
        # Set Role
        if role == 'admin':
            user.is_staff = True
        
        user.save()
        
        # Success! Send them to login
        return redirect('login_user')

    return render(request, 'signup.html')

@login_required
def employee_dash(request):
    # 1. Get the filter value from the URL (e.g., ?priority=High)
    priority_filter = request.GET.get('priority')
    
    # 2. Start with all active tasks for this user
    tasks = Task.objects.filter(assigned_to=request.user, is_completed=False)
    
    # 3. If a specific priority was clicked, narrow down the list
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    return render(request, 'employee_dashboard.html', {
        'tasks': tasks,
        'active_filter': priority_filter # Send this back to highlight the active button
    })

from .forms import TaskForm

@user_passes_test(is_admin)
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'title': 'Add New Task'})

@user_passes_test(is_admin)
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'title': 'Edit Task'})

@user_passes_test(is_admin)
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_confirm.html', {'task': task}) # Fallback

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        new_username = request.POST.get('username')
        
        # 1. Check if the username is taken by ANOTHER user
        if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            messages.error(request, "This username is already taken.")
            return render(request, 'edit_profile.html')

        # 2. Update all fields
        user.username = new_username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        
        # Redirect based on role
        if user.is_staff:
            return redirect('admin_dashboard')
        return redirect('employee_dashboard')
        
    return render(request, 'edit_profile.html')

def admin_dashboard(request):
    query = request.GET.get('search')
    if query:
        all_tasks = Task.objects.filter(title__icontains=query)
    else:
        all_tasks = Task.objects.all()
    return render(request, 'dashboard.html', {'tasks': all_tasks})


def logout_user(request):
    logout(request)
    return redirect('login_user')



