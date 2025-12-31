from django.urls import path
from .views import (
    register_view,
    home_view,
    login_view,
    logout_view,
    teacher_dashboard,
    admin_dashboard,
    student_profile,
    student_courses,
)
from .views import Create


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/profile/', student_profile, name='student_profile'),
    path('student/courses/', student_courses, name='student_courses'),
    
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('hero/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', Create.as_view(), name='student_dashboard'),
]
