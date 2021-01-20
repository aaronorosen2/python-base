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

    def __str__(self):
        return self.name


class Class(models.Model):
    class_name = models.CharField(max_length=128,blank=True,null=True)
    class_id = models.CharField(max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name

class ClassEnrolled(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} {self.class_enrolled}"