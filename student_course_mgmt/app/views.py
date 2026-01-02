from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.views import View
from .models import Student
from django.utils.decorators import method_decorator


# ------------------ HOME ------------------
def home_view(request):
    return render(request, 'accounts/index.html')


# ------------------ REGISTER ------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # ❌ REMOVED: Auto-creating Student here was breaking logic
            # Student.objects.create(user=user)

            login(request, user)
            return redirect('student_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# ------------------ LOGIN ------------------
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


# ------------------ LOGOUT ------------------


@login_required
def logout_confirm(request):
    return render(request, 'accounts/logout.html')

@login_required
def perform_logout(request):
    logout(request)  
    return redirect('login')  





# ------------------ STUDENT PROFILE ------------------
@login_required
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # ✅ CHANGED: force profile creation if not exists
        return redirect('student_create')

    return render(request, 'student/profile.html', {'student': student})


# ------------------ STUDENT COURSES ------------------
@login_required
def student_courses(request):
    return render(request, 'student/my_courses.html')


# ------------------ ADMIN DASHBOARD ------------------
@login_required
def admin_dashboard(request):
    return render(request, 'hero/dashboard.html')


# ------------------ TEACHER DASHBOARD ------------------
@login_required
def teacher_dashboard(request):
    if not request.user.groups.filter(name='Teacher').exists():
        raise PermissionDenied
    return render(request, 'teacher/dashboard.html')


# ------------------ STUDENT DASHBOARD ------------------
@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


# =====================================================
# =============== STUDENT CREATE VIEW =================
# =====================================================

@method_decorator(login_required, name='dispatch')
class StudentCreateView(View):

    def get(self, request):
        # ✅ CHANGED: Block access if profile already exists
        if Student.objects.filter(user=request.user).exists():
            return redirect('student_profile')

        return render(request, 'student/create.html')

    def post(self, request):
        # ✅ CHANGED: Same protection for POST
        if Student.objects.filter(user=request.user).exists():
            return redirect('student_profile')

        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        address = request.POST.get('address')

        # ✅ Validation
        if not all([name, age, email, grade, address]):
            return render(request, 'student/create.html', {
                'error': 'All fields are required'
            })

        # ✅ Email uniqueness check
        if Student.objects.filter(email=email).exists():
            return render(request, 'student/create.html', {
                'error': 'Email already exists'
            })

        # ✅ CHANGED: CREATE student ONLY here
        Student.objects.create(
            user=request.user,
            name=name,
            age=int(age),
            email=email,
            grade=int(grade),
            address=address
        )

        return redirect('student_profile')
