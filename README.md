# Employee Task Management System

A full-stack employee task management application built with Django and Django REST Framework. 
The system allows administrators to manage employees and assign, track, and update tasks efficiently.

## 🚀 Live Demo

https://employee-task-management-site.onrender.com

## 📌 Features

- User authentication using Django REST Framework Token Authentication
- Employee management
- Create, assign, update, and delete tasks
- Task status tracking
- RESTful APIs
- API documentation using Swagger
- CSRF protection
- Responsive frontend interface
- SQLite database support

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite
- Django REST Framework Spectacular (Swagger API Documentation)

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Render
- Gunicorn
- WhiteNoise

## 📂 Project Structure
employee-task-management-system/
│
├── manage.py
├── requirements.txt
├── Procfile
│
├── company_site/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│
└── members/
├── models.py
├── views.py
├── serializers.py
└── urls.py


## ⚙️ Installation and Setup

Clone the repository:

```bash
git clone https://github.com/UmangJayaswal/employee-task-management-system.git

Navigate into the project:
cd employee-task-management-system

Create a virtual environment:
python -m venv venv

Activate it:
Windows:
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

The application will be available at:
http://127.0.0.1:8000/

📖 API Documentation

Swagger documentation is available at:

/api/docs/

🗄️ Database

The project currently uses SQLite for development and deployment.

📸 Screenshots

##Create Account Page
(screenshots/CreateAccount.png)

##Sign In Page
(screenshots/SignIn.png)

##Employee Dashboard Page
(screenshots/EmployeeDashboard.png)

##Add New Task 
(screenshots/AddNewTask.png)

##Edit Task
(screenshots/EditTask.png)

##Employee Dashboard Page
(screenshots/EmployeeDashboard.png)

##Admin Profile Settings
(screenshots/AdminProfileSettings.png)

👨‍💻 Author

Umang Jayaswal

GitHub:
https://github.com/UmangJayaswal