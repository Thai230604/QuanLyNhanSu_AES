# Generated by Django 4.2.17 on 2024-12-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_remove_employee_department_remove_employee_hire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='birth_date',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
