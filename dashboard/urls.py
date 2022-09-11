from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="dashboard_index"),
    path('all_student', views.all_student, name="all_student"),
    path('student_by_year/<int:id>', views.student_by_year, name="student_by_year"),
    path('active_lesson', views.active_lesson, name="active_lesson"),
    path('upload_video', views.upload_video, name="upload_video"),
    path('update_video', views.update_video, name="update_video"),
    path('courses_admin', views.courses_admin, name='courses_admin'),
    path('units', views.units, name='units'),
    path('branchs', views.branchs, name='branchs'),
    path('add_branch', views.add_branch, name='add_branch'),
    path('add_unit', views.add_unit, name='add_unit'),
    path('exams_admin', views.exams_admin, name='exams_admin'),
    path('add_quiz', views.add_quiz, name='add_quiz'),
    path('update_quiz/<int:id>', views.update_quiz, name='update_quiz'),
    path('add_question/<int:id>', views.add_question, name='add_question'),
    path('money',views.money, name='money'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('watch', views.watch, name='watch'),
    
    path('ajax/load/ajax_load_year_branchs',views.ajax_load_year_branchs, name='ajax_load_year_branchs'),
    path('ajax/load/ajax_load_year_units',views.ajax_load_year_units, name='ajax_load_year_units'),
    path('ajax/load/ajax_load_year_lessons',views.ajax_load_year_lessons, name='ajax_load_year_lessons'),
    path('ajax/load/ajax_load_form_update_student', views.ajax_load_form_update_student, name='ajax_load_form_update_student'),
    path('ajax/load/ajax_load_form_update_video',views.ajax_load_form_update_video, name='ajax_load_form_update_video'),
    path('ajax/load/ajax_load_form_update_unit',views.ajax_load_form_update_unit, name='ajax_load_form_update_unit'),
    path('ajax/load/ajax_load_form_update_branch',views.ajax_load_form_update_branch, name='ajax_load_form_update_branch'),

    path('status_video/<str:token>', views.status_video, name='status_video'),
] 


