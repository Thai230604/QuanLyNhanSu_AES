from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encrypt/', views.encrypt, name='encrypt'), 
    path('decrypt/', views.decrypt, name='decrypt'), 
    path('add/', views.add, name='add'),
    # path('employee_list/', views.employee_list, name='employee_list'),
    path('department/<int:department_id>/employees/', views.employee_list, name='employee_list'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employee_update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('departments/', views.department_list, name='department_list'),
    path('department/<int:department_id>/employees/decrypt/', views.employee_decrypt, name='employee_decrypt'),

]

