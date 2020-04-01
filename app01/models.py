from django.db import models
import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'user_manager.settings.py')





class classes(models.Model):
    id=models.CharField(max_length=32,primary_key=True)
    caption = models.CharField(max_length=32)


class student(models.Model):
    name = models.CharField(max_length=32)
    cls = models.CharField(max_length=32)
    emile = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    student_id=models.CharField(max_length=32,primary_key=True)

class teacher(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ManyToManyField('classes')


class administrator(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    name= models.CharField(max_length=32)
    emile= models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    unique_id=models.CharField(max_length=32)
    identity=models.CharField(max_length=32,primary_key=True)
    gender = models.CharField(max_length=32)



