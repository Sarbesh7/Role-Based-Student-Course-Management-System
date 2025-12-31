from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    grade= models.IntegerField()
    address=models.CharField(max_length=255)
    age=models.IntegerField()
    
    