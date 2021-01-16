from django.db import models


# class Teacher(models.Model):
#    email = models.EmailField(max_length=254, blank=True, null=True)
#    name = models.CharField(max_length=128, blank=True, null=True)
#    phone = models.CharField(max_length=20, null=True)
#    created_at = models.DateTimeField(auto_now=True)


class Student(models.Model):
    # XXX NEed to link in user model object
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now=True)
