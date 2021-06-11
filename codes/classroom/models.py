from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    # XXX NEed to link in user model object
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='usernames')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teachername')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher} {self.student}"


class TeacherAccount(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='teacherinfo')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.teacher} {self.active}"

class Class(models.Model):
    class_name = models.CharField(max_length=128, blank=True, null=True)
    # invite_id = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)

    def __str__(self):
        return self.class_name

class InviteClass(models.Model):
    class_invited = models.ForeignKey(Class, on_delete=models.CASCADE)
    uuid = models.TextField(null=False, blank=False, unique=True)
    def __str__(self):
        return f"{self.class_invited} {self.uuid}"

class ClassEnrolled(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} {self.class_enrolled}"


class ClassEmailAlert(models.Model):
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_enrolled

class ClassSMSAlert(models.Model):
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_enrolled

class StudentEmailAlert(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name

class StudentSMSAlert(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name