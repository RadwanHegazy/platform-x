from . import views
from django.urls import path

urlpatterns = [

    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('add-student/',views.add_Student,name='add_student'),
    path('student-register/<str:teacher_uuid>/',views.student_register,name='student_register'),
    path('student/search/',views.student_result_search,name='student_search'),
    path('student/<str:stuuid>/',views.student_details,name='student_details'),
    path('change-password/',views.change_password,name='change_password'),
    path('edit/student/<str:stuuid>',views.edit_student,name='edit_student'),
    path('edit/student/<str:stuuid>/confrim',views.edit_student_data,name='edit_student_data'),
    path('exam/',views.create_exam,name='create_exam'),
    path('exam/<int:examid>/<str:teacher_uuid>/',views.exam_results,name='exam_results'),
    path('exams/',views.exams,name='exams'),
    path('collect-marks/',views.collect_marks,name='collect_marks'),
    path('teacher-register/',views.teacher_register,name='teacher_register')
]

