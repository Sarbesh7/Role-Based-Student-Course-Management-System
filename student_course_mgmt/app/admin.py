from django.contrib import admin
from .models import Student, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'grade', 'age')
    search_fields = ('name', 'email')
    list_filter = ('grade',)
    ordering = ('id',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'grade', 'description')
    search_fields = ('course_name',)
    list_filter = ('grade',)
    ordering = ('id',)