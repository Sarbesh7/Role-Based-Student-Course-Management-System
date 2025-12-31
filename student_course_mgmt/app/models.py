from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name or self.user.username
