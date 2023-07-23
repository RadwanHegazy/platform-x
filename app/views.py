import random
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.views import auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Month, Exam, Result, LEVELS, Teacher
import datetime
import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Project.settings import ADMIN_URL_NAME




def teacher_register (request) :

    if request.method == "POST" :
        name = request.POST['name']
        subject = request.POST['subject']
        wa_number = request.POST['wa_number']
        image = ''

        if 'image' in request.FILES :
            image = request.FILES['image']
        
        t = Teacher.objects.create(
            name = name,
            subject = subject,
            wa_number = wa_number,
        )

        if image :
            t.image = image
        
        t.save()

        messages.success(request,'جاري تجهيز المنصة الخاصة بك و سيتم التواصل معك خلال 24 ساعة')

        return redirect('teacher_register')

    return render(request,'platform-x/teacher-register.html')


def home (request) :

    if request.user.is_superuser:
        return redirect(f'{ADMIN_URL_NAME}/')
    
    if request.user.is_authenticated == False :
        return render(request,'platform-x/landing-page.html')

    # getNames = pd.read_excel('app/data.xlsx',usecols='A')
    # getCodes = pd.read_excel('app/data.xlsx',usecols='B')
    
    # names = []
    # codes = []

    # for key, val in getNames.to_dict().items() :
    #     for k, v in val.items () :
    #         names.append(v)
    # for key, val in getCodes.to_dict().items() :
    #     for k, v in val.items () :
    #         codes.append(v)

    # for i in range(len(codes)) :

    #     Student.create_student(
    #         name = names[i],
    #         code = codes[i],
    #         level =[i[0] for i in LEVELS][0],
    #         parent_phone = int(1009675007),
    #     ).save()
    

    # print('Done')


    if 'delete' in request.GET :
        st = Student.objects.filter(student_uuid = request.GET['delete'])
        st.first().delete()
        return redirect('home')

    students = Student.objects.all()
    current_month = datetime.datetime.now().month
    
    months_list = [
        8,9,10,11,12,1,2,3,4,5,6,7
    ]

    context = {
        'students' : students,
        'current_month':current_month,
        'months' : Month.objects.all(),
        'months_list':months_list,
    }

    if 'select_month' in request.GET :
        m = int(request.GET['select_month'])
        context['months'] = Month.objects.filter(name=m)
        context['current_month'] = m

    if 'level' in request.GET :
        level = request.GET['level']

        if level != 'all' :
            students = Student.objects.filter(level=level)
            context['current_level'] = level
            context['students'] = students
        else :
            context['current_level'] = 'all'
    
    if 'search' in request.GET :
        query = request.GET['search']
        if query :
            try :
                query = int(query)
                context['students'] = Student.objects.filter(code = query)
            except :
                context['students'] = Student.objects.filter(name__icontains = query)


    page = request.GET.get('page', 1)

    paginator = Paginator(context['students'], 25)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context['students'] = students


    return render(request,'home.html',context)



@login_required
def collect_marks (request) :

    context = {
        'current_level' : ''
    }


    if request.method == "POST" : 
        
        level = request.POST['level']
        exams_range = int(request.POST['exam_range']) 
        
        context['range'] = exams_range
        context['current_level'] = level
        
        students = Student.objects.filter(level=level)
        exams = Exam.objects.filter(level = level).order_by('-date')[0:exams_range]

        studentMarks = []
        final_mark = 0

        if  exams_range > exams.count():
            messages.warning(request,'لا يوجد عدد امتحانات مطابق')
        
        else :
        
            for exam in exams :
                final_mark += exam.final_mark
            
            for student in students :
                student_total_marks = 0
                for exam in exams :
                    try : 
                        res = Result.objects.get(student=student,exam=exam)
                        student_total_marks += res.mark
                    except Result.DoesNotExist :
                        pass

                studentMarks.append({
                    'name':student.name,
                    'mark' : f'{ student_total_marks } / {final_mark}'
                })
            
            context['students'] = studentMarks
        


        


    return render(request,'collect-marks.html',context)



@login_required
def add_Student (request) :

    
    if request.method == "POST" :
        name = request.POST['name']
        code = request.POST['code']
        parent_phone = request.POST['parent_phone']
        level = request.POST['level']
        

        if code == '' :

            while True :
                generated_code = random.randint(100,10000)
                check = Student.objects.filter(code=generated_code)
                if check.exists() is not True :
                    code = generated_code
                    break
        

        st = Student.create_student(
            name = name,
            code = code,
            parent_phone = parent_phone,
            level = level
        )

        messages.success(request,'تمت اضافة الطالب بنجاح')
        
        return redirect('add_student')

    return render(request,'add-student.html')



def levels (request) : 

    context =  {
        'levels' : [i[0] for i in LEVELS]
    }

    return context


@login_required
def change_password (request) :
    
    context = {}

    if request.method == "POST" :
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 :
            user = request.user
            user.set_password(password1)
            user.save()
            auth_login(request,user)
            return redirect('home')
        else :
            context['msg'] = 'كلمة المرور غير متطابقة'
            
    return render(request,'change-password.html',context)

@login_required
def edit_student( request,stuuid ) :
    
    student = get_object_or_404(Student,student_uuid = stuuid)

    if 'paid' in request.GET:
        paid = request.GET['paid']
        m = Month.objects.get(id = paid)
        m.is_paid = True
        m.paid_date = datetime.datetime.now().date()
        m.save()
        return redirect('edit_student',stuuid)

    if 'del' in request.GET :
        student.delete()
        return redirect('home')


    


    if  request.method == "POST" :
        
        student_mark = request.POST['student_mark']
        final_mark = request.POST['final_mark']
        
        ex = Exam.objects.create(final_mark=final_mark,level=student.level)
        ex.save()

        res = Result.objects.create(exam = ex, student = student, mark = student_mark)
        res.save()
        
        return redirect('edit_student',stuuid)



    months = Month.objects.filter(student = student)
    current_date = datetime.datetime.now().date
    
    context = {
        'student' : student,
        'months' : months,
        'results': Result.objects.filter(student = student).order_by('-id'),
        'current_date' : current_date,
    }
    return render(request,'student.html',context)
  
@login_required
def edit_student_data (request, stuuid) :
    student = get_object_or_404(Student, student_uuid = stuuid)
    level = request.POST['level']
    name = request.POST['name']
    parent_phone = request.POST['parent_phone']

    student.name = name
    student.level = level
    student.parent_phone = f'https://wa.me/+20' + parent_phone
    student.save()

    return redirect('edit_student',stuuid)

@login_required
def create_exam(request) :

    if request.method == "POST" :
        level = request.POST['level']
        final_mark = request.POST['final_mark']

        exam = Exam.objects.create(level=level,final_mark=final_mark)
        exam.save()

        return redirect('exam_results',exam.id)

    return render(request,'create-exam.html')


def exam_results (request,examid) :
    
    exam = get_object_or_404(Exam, id = examid)
    students = Student.objects.filter(level = exam.level )
    
    if students.count() != Result.objects.filter(exam=exam).count() :
        for st in students :
            if Result.objects.filter(exam=exam,student=st).exists() is not True :
                res = Result.objects.create(student = st,exam=exam,mark=0)
                res.save()

    context = {
        'exam' : exam,
        'students' : students,
        'results' : Result.objects.filter(exam = exam).order_by('-mark'),
    }

        

        
    if request.method == "POST" :
        
        students_ids = str(request.POST['ids']).split('&')
        students_results = str(request.POST['results']).split('&')


        for i in range(len(students_ids)) :
            if students_ids[i] :
                st = Student.objects.get(id = students_ids[i])
                result = students_results[i]
                if Result.objects.filter(student = st, exam = exam, mark = result).exists() == False :
                    
                    if int(result) <= int(exam.final_mark) :
                        res = Result.objects.get(
                            student = st ,
                            exam = exam,
                        )

                        res.mark = result

                        res.save()
                    

        
        return redirect('exam_results',examid)


    if request.user.is_authenticated:
        return render(request,'exam-results.html',context)
    else:
        return render(request,'exam-results-visitro.html',context)


def exams (request) :


    
    context = {
        'current_level' : [i[0] for i in LEVELS],
        'exams' : Exam.objects.filter(level = [i[0] for i in LEVELS]).order_by('-date')
    }



    if request.method == "POST" :
        context['current_level'] = request.POST['level']
        context['exams'] = Exam.objects.filter(level = request.POST['level']).order_by('-date')

    return render(request,'exams.html',context)


def student_register (request) :

    if  request.method == "POST" :
        
        name = request.POST['name']
        level = request.POST['level']
        parent_phone = request.POST['parent_phone']


        while True :
            generated_code = random.randint(100,10000)
            check_code = Student.objects.filter(code=generated_code)

            if check_code.exists() is not True :
                Student.create_student(name=name,level=level,code=generated_code,parent_phone=parent_phone)
                break
            
        messages.success(request,'تمت اضافتك بنجاح علي المنصة')

        return redirect('student_register')

    return render(request,'student-register.html')
    
    


def student_result_search (request) :
    
    if request.method == "POST" :
        code = request.POST['code']

        student = Student.objects.filter(code = code)
        
        if student.exists ():
            student = student.first()
            return redirect('student_details',student.student_uuid)
        else :
            messages.info(request,'لا يوجد طالب يحمل هذا الكود')
            return redirect('student_search')

    return render(request,'student-details-search.html')

def student_details (request,stuuid) :
    student = get_object_or_404(Student,student_uuid = stuuid)

    context = {
        'student' : student,
        'months' : Month.objects.filter(student = student).order_by('id'),
        'results' : Result.objects.filter(student = student).order_by('-id'),
    }


    return render(request,'student-details.html',context)

def login (request) :

    context = {}

    if request.method == "POST" :

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username)
        if user.exists() :
            
            user = user.first()
            auth = authenticate(username = user.username, password = password)

            if auth is not None :
                auth_login(request,user)
                return redirect('home')
            else :
                context['msg'] = 'كلمة المرور غير صحيحة'

        else :
            context['msg'] = 'هذا المستخدم غير موجود'

    return render(request,'login.html',context)