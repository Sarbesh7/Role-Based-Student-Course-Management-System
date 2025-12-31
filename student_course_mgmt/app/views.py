from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
# for the csrf error while logging in due to not refreshing the page
from django.views import View
from .models import Student
from django.utils.decorators import method_decorator


def home_view(request):
    return render(request, 'accounts/index.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@never_cache
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ROLE-BASED REDIRECT (safe defaults)
            
            if user.is_staff:
                return redirect('admin_dashboard')
            
            if user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard') 
            
            return redirect('student_dashboard')

        error = "Invalid credentials"

    return render(request, 'accounts/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required
# def student_dashboard(request):
#     return render(request, 'student/dashboard.html')

@login_required
def student_profile(request):
    return render(request, 'student/profile.html')

@login_required
def student_courses(request):
    return render(request, 'student/my_courses.html')



@login_required
def admin_dashboard(request):
    return render(request, 'hero/dashboard.html')

@login_required
def teacher_dashboard(request):
    print("TEACHER DASHBOARD HIT")
    print("User:", request.user.username)
    print("Groups:", request.user.groups.all())

    if not request.user.groups.filter(name='Teacher').exists():
        raise PermissionDenied

    return render(request, 'teacher/dashboard.html')


@method_decorator(login_required, name='dispatch')
class Create(View):

    def get(self, request):
        students = Student.objects.all()
        return render(request, 'student/dashboard.html', {'students': students})

    def post(self, request):
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        address = request.POST.get('address')

        if not all([name, age, email, grade, address]):
            return render(request, 'student/dashboard.html', {
                'error': 'All fields are required'
            })

        if Student.objects.filter(email=email).exists():
            return render(request, 'student/dashboard.html', {
                'error': 'Email already exists'
            })

        Student.objects.create(
            name=name,
            age=int(age),
            email=email,
            grade=int(grade),
            address=address
        )

        return redirect('student_dashboard')