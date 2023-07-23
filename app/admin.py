from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student, Exam, Result, Month, Teacher




# add on admin
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Result)
admin.site.register(Month)
admin.site.register(Exam)

# remove from admin
admin.site.unregister(Group)