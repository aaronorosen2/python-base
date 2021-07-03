from django.contrib import admin
from .models import Student, Teacher, TeacherAccount

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone')
    fields = ['email', 'name', 'phone']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'created_at')
    fields = ['teacher', 'student']

@admin.register(TeacherAccount)
class TeacherAccountAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'active')
    fields = ['teacher', 'active']

# admin.site.register(Student)
# admin.site.register(Teacher)
# admin.site.register(TeacherAccount)
