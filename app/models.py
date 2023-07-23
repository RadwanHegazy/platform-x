from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid, threading

LEVELS = (
    ('1 ث','1 ث'),
    ('2 ث','2 ث'),
    ('3 ث','3 ث'),
)



class Teacher(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    image = models.FileField(default='default.png',upload_to='teacher-images/')
    wa_number = models.URLField(default='')
    is_online = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateField(null=True,blank=True)
    expired_at = models.DateField(null=True,blank=True)
    teacher_uuid = models.CharField(max_length=10000,null=True,blank=True)

    def __str__(self) :
        return f'{self.name} | Paid : {self.is_paid}'
    



class Student (models.Model) :
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    code = models.IntegerField()
    parent_phone = models.URLField()
    level = models.CharField(choices=LEVELS,max_length=100)
    student_uuid = models.CharField(max_length=1000)

    def __str__(self) :
        return f"{self.name}"

    def create_student (**info) :
        name = info['name']
        code = info['code']
        parent_phone = info['parent_phone']
        level = info['level']
        teacher = info['teacher']

        st = Student.objects.create(
            name = name,
            code = code,
            parent_phone = f'https://wa.me/+20' + f'{parent_phone}',
            level = level,
            teacher = teacher,
            student_uuid = uuid.uuid4()
        )

        st.save()

        return st


class Month (models.Model) :
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    name = models.IntegerField()
    paid_date = models.DateField(blank=True,null=True)

    def __str__(self) :
        return f'{self.student.name} , {self.name}, {self.is_paid}'
    
    def create_student_months (student) :

        current_moth = 7
        for i in range(0,12) :
            current_moth = current_moth + 1
            if current_moth > 12 :
                current_moth = 1 
            
            Month.objects.create(
                student = student,
                name = current_moth
            ).save()



class Exam (models.Model) :
    date = models.DateField(auto_now_add=True)
    level = models.CharField(max_length=100,choices=LEVELS)
    final_mark = models.IntegerField(blank=True,null=True)

    def __str__(self) :
        return f'{self.date} for {self.level}'


class Result (models.Model) :
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    mark = models.IntegerField()

    def __str__(self) :
        return f"{self.student}, {self.mark} / {self.exam.final_mark}"
    



@receiver(post_save, sender=Teacher)
def create_teacher_uuid(sender, instance, created, **kwargs):
    if created:
        teacher_uuid = uuid.uuid4()
        instance.teacher_uuid = teacher_uuid
        instance.wa_number = 'https://wa.me/+20' + f'{instance.wa_number}'
        instance.save()


@receiver(post_save, sender=Student)
def create_moths(sender, instance, created, **kwargs):
    if created:
        current_moth = 7
        for i in range(0,12) :
            current_moth = current_moth + 1
            if current_moth > 12 :
                current_moth = 1 
            
            Month.objects.create(
                student = instance,
                name = current_moth
            ).save()
            

