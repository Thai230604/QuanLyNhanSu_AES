from django.contrib import admin

# Register your models here.
from .models import Department, Employee

# Đăng ký mô hình Department và Employee
admin.site.register(Department)
admin.site.register(Employee)