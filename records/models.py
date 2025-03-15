from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    department_code = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_code = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    birth_date = birth_date = models.CharField(max_length=20, null=False)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.employee_code})"
