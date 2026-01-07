from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.views import View
from .models import Student, Course
from django.utils.decorators import method_decorator
# Home
def home_view(request):
    return render(request, 'accounts/index.html')


# Register
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# Login
@never_cache
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            if user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')

            return redirect('student_dashboard')

        error = "Invalid credentials"

    return render(request, 'accounts/login.html', {'error': error})


# Logout
@login_required
def logout_confirm(request):
    return render(request, 'accounts/logout.html')

@login_required
def perform_logout(request):
    logout(request)  
    return redirect('login')  

# Student profile
@login_required
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('student_create')

    return render(request, 'student/profile.html', {'student': student})


# Student courses
@login_required
def student_courses(request):
    student = Student.objects.filter(user=request.user).first()
    if not student or student.grade is None:
        return render(request, 'student/my_courses.html', {
            'courses': [],
            'info': 'Create your profile to see courses.'
        })
    courses = Course.objects.filter(grade=student.grade)
    return render(request, 'student/my_courses.html', {'courses': courses})


# Admin dashboard
@login_required
def admin_dashboard(request):
    users = User.objects.all()
    
    user_data = []
    for u in users:
        if u.is_staff:
            role = 'Admin'
        elif u.groups.filter(name='Teacher').exists():
            role = 'Teacher'
        else:
            role = 'Student'
        user_data.append({
            'id': u.id,
            'username': u.username,
            'role': role  })
        
    students = Student.objects.all()
    return render(request, 'hero/dashboard.html', {'students': students, 'users': user_data})

@login_required
def delete_page(request, id):
    if not request.user.is_staff:
        raise PermissionDenied

    student = get_object_or_404(Student, id=id)
    return render(request, 'hero/delete_student.html', {'student': student})
@login_required 
def delete_student(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    student = get_object_or_404(Student, id=id)

    # Only allow deletion via POST; otherwise send to confirm page
    if request.method != 'POST':
        return redirect('delete_confirm', id=id)

    student.delete()
    return redirect('admin_dashboard')
    

# Teacher dashboard
@login_required
def teacher_dashboard(request):
    students = Student.objects.all()
    if not request.user.groups.filter(name='Teacher').exists():
        raise PermissionDenied
    courses = Course.objects.all()
    return render(request, 'teacher/dashboard.html', {
        'students': students,
        'courses': courses,
    })

# User deletion
@login_required
def delete_page_user(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    user = get_object_or_404(User, id=id)
    return render(request, 'hero/delete_user.html', {'user': user})


@login_required
def delete_user(request,id):
    if not request.user.is_staff:
        raise PermissionDenied
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_dashboard')   

# Student dashboard
@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


# Student create
@method_decorator(login_required, name='dispatch')
class StudentCreateView(View):

    def get(self, request):
        if Student.objects.filter(user=request.user).exists():
            return redirect('student_profile')

        return render(request, 'student/create.html')

    def post(self, request):
        if Student.objects.filter(user=request.user).exists():
            return redirect('student_profile')

        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        address = request.POST.get('address')

        if not all([name, age, email, grade, address]):
            return render(request, 'student/create.html', {
                'error': 'All fields are required'
            })

        # Email uniqueness check
        if Student.objects.filter(email__iexact=email).exists():
            return render(request, 'student/create.html', {
                'error': 'Email already exists'
            })

        Student.objects.create(
            user=request.user,
            name=name,
            age=int(age),
            email=email,
            grade=int(grade),
            address=address
        )

        return redirect('student_profile')
    
@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        grade = request.POST.get("grade")
        address = request.POST.get("address")

        # Prevent duplicate email across students
        if email and Student.objects.filter(email__iexact=email).exclude(id=student.id).exists():
            template = "hero/update_student.html" if request.user.is_staff else "teacher/update_student.html"
            return render(request, template, {"student": student, "error": "Email already exists"})

        student.name = name
        student.age = age
        student.email = email
        student.grade = grade
        student.address = address

        student.save()
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("teacher_dashboard")

    
    if request.user.is_staff:
        return render(request, "hero/update_student.html", {"student": student})
    return render(request, "teacher/update_student.html", {"student": student})


@method_decorator(login_required, name='dispatch')
class CourseCreateView(View):
    
    def get(self,request):
        return render(request,'teacher/course_students.html')
    
    def post(self,request):
        grade=request.POST.get('grade')
        course_name=request.POST.get('course_name')
        description=request.POST.get('description')
        
        Course.objects.create(
            grade=int(grade),
            course_name=course_name,
            description=description,
        )
        return redirect('teacher_dashboard')