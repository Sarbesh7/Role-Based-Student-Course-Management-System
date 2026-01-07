


from django.urls import path
from .views import (
    register_view,
    home_view,
    login_view,
    logout_confirm,
    perform_logout,
    teacher_dashboard,
    admin_dashboard,
    student_dashboard,
    student_profile,
    student_courses,
    StudentCreateView,
    update_student,
    CourseCreateView,
    delete_student,
    delete_page,
    delete_user,
    delete_page_user,
    
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_confirm, name='confirm'),
    path('logout/perform/', perform_logout, name='logout'),

    path('student/profile/', student_profile, name='student_profile'),
    path('student/courses/', student_courses, name='student_courses'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/create/', StudentCreateView.as_view(), name='student_create'),

    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/update/<int:id>/', update_student, name='update_student'),
    path('teacher/course/', CourseCreateView.as_view(), name='Course'),
    
    path('hero/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('hero/delete/<int:id>/', delete_student, name='delete'),
    path('hero/delete/<int:id>/confirm/', delete_page, name='delete_confirm'),
    path('hero/delete_user/<int:id>/', delete_user, name='delete_user'),
    path('hero/delete_user/<int:id>/confirm/', delete_page_user, name='delete_user_confirm'),
    
    
]
