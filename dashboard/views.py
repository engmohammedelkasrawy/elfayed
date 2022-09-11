from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.forms import inlineformset_factory
from student.models import Student, RegisterVideo,Watched
from student.forms import StudentCreationForm, UpdateStudentForm,UserCreationForm,UpdateUserForm
from courses.models import Lesson,Branch,Unit
from courses.forms import AddBranch, AddUnit,AddLesson
from edu.models import Year
from exam.models import Quiz,Question,Answer,Result
from exam.forms import QuizCreationForm,QuestionCreationForm
from datetime import date, timedelta
from .utils import upload_video_serve
from django.core.mail import send_mail
from django.conf import settings
import os
import json
import requests
from requests_toolbelt import MultipartEncoder
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@user_passes_test(lambda u: u.is_staff)
def index(request):
    student_year1 = Student.objects.filter(year_id=1)
    student_year2 = Student.objects.filter(year_id=2)
    student_year3 = Student.objects.filter(year_id=3)
    all_lessons = Lesson.objects.all()
    all_quiz=Quiz.objects.all()

    lesson_not_active = RegisterVideo.objects.filter(active=False)
    context={
        "title":"لوحة التحكم",
        "student_year1":student_year1,
        "student_year2": student_year2,
        "student_year3":student_year3,
        "all_lessons":all_lessons,
        "all_quiz":all_quiz,
        "lesson_not_active":lesson_not_active,
    }
    return render(request, "dashboard/index.html",context)


@user_passes_test(lambda u: u.is_staff)
def all_student(request):
    students = Student.objects.all().order_by('-created')
    if "update" in request.POST:
        student_id = request.POST.get('student')
        user_id = request.POST.get('user')
        student = get_object_or_404(Student, id=student_id)
        user = get_object_or_404(User, id=user_id)
        user_form = UpdateUserForm(request.POST, instance=user)
        student_form = UpdateStudentForm(request.POST ,instance=student)
        if user_form.is_valid and student_form.is_valid:
            user_form.save()
            student_form.save()
    elif "delete" in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        
        
    context = {
        "title": "جميع الطلاب",
        "students":students,
    }
    return render(request, "dashboard/all_student.html",context)


@user_passes_test(lambda u: u.is_staff)
def student_by_year(request,id):
    year=get_object_or_404(Year,id=id)
    students = Student.objects.filter(year_id=year).order_by('-created')
    if "delete" in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()

    if "update" in request.POST:
        student_id = request.POST.get('student')
        user_id = request.POST.get('user')
        student = get_object_or_404(Student, id=student_id)
        user = get_object_or_404(User, id=user_id)
        user_form = UpdateUserForm(request.POST, instance=user)
        student_form = UpdateStudentForm(request.POST ,instance=student)
        if user_form.is_valid and student_form.is_valid:
            user_form.save()
            student_form.save()

    context = {
        "title": f"طلاب الصف {year}",
        "students":students,
    }
    return render(request, "dashboard/student_by_year.html", context)


@user_passes_test(lambda u: u.is_staff)
def active_lesson(request):
    lesson_Anactie=RegisterVideo.objects.filter(active=False).order_by('created')
    
    if "done" in request.POST:
        lesson=get_object_or_404(RegisterVideo,id=request.POST.get("lesson_id"))
        lesson.active=True
        lesson.save()

    
    if "rejected" in request.POST:
        lesson = RegisterVideo.objects.get(id=request.POST.get("lesson_id"))
        lesson.delete()
        

    context = {
        "title": "تفعيل الدروس",
        "lesson_Anactie":lesson_Anactie,
        
    }
    return render(request, "dashboard/active_lesson.html",context)


@user_passes_test(lambda u: u.is_staff)
def courses_admin(request):
    lessons = Lesson.objects.all().order_by('-created')
    if request.method=="POST":
        lesson = get_object_or_404(Lesson, id=request.POST.get("lesson_id"))
        url = "https://dev.vdocipher.com/api/videos"
        querystring = {"videos": f"{lesson.video_id}"}
        headers = {
            'Authorization': "Apisecret DzJNvBi24Htggyg5HpvDPpex6YAKIgbMNaRbPV5mImVUCM1ds3WMUR9PpcGM1wd6",
            'Content-Type': "application/json",
            'Accept': "application/json"
        }
        response = requests.request("DELETE", url, headers=headers, params=querystring)
        lesson.delete()
    
    context = {
        "title": "ادارة الفيديوهات",
        "lessons": lessons,
    }
    return render(request, "dashboard/courses_admin.html", context)


@user_passes_test(lambda u: u.is_staff)
def units(request):
    all_units=Unit.objects.all()
    if "update" in request.POST:
        unit = get_object_or_404(Unit, id=request.POST.get("unit_id"))
        form=AddUnit(request.POST , instance=unit)
        if form.is_valid():
            form.save()
        

    if "delete" in request.POST:
        unit = get_object_or_404(Unit, id=request.POST.get("unit_id"))
        unit.delete()

    context = {
        "title": "ادارة الفيديوهات",
        "all_units": all_units,
    }
    return render(request, "dashboard/units.html", context)


@user_passes_test(lambda u: u.is_staff)
def branchs(request):
    all_branchs = Branch.objects.all()
    if "update" in request.POST:
        branch = get_object_or_404(Branch, id=request.POST.get("branch_id"))
        form = AddBranch(request.POST, instance=branch)
        if form.is_valid():
            form.save()

    if "delete" in request.POST:
        branch = get_object_or_404(Branch, id=request.POST.get("branch_id"))
        branch.delete()

    context = {
        "title": "ادارة الفيديوهات",
        "all_branchs": all_branchs,
    }
    return render(request, "dashboard/branchs.html", context)
    pass



@user_passes_test(lambda u: u.is_staff)
def upload_video(request):
    if request.method=="POST":
        ############# STEP 1 ####################
        video_name = request.POST.get("name")
        querystring = {"title": video_name}
        url = "https://dev.vdocipher.com/api/videos"
        api_secret_key = "DzJNvBi24Htggyg5HpvDPpex6YAKIgbMNaRbPV5mImVUCM1ds3WMUR9PpcGM1wd6"
        headers = {
            'Authorization': "Apisecret " + api_secret_key
        }
        response = requests.request("PUT", url, headers=headers, params=querystring)
        uploadInfo = response.json()
        video_id = uploadInfo['videoId']
        get_unit = Unit.objects.get(id=request.POST.get("unit"))
        createLesson=Lesson.objects.create(name=video_name,video_id=video_id,unit=get_unit)
        response.raise_for_status()
        return JsonResponse(uploadInfo,safe=False)
    context = {
        "title": "اضق الدروس",
        
    }
    return render(request, "dashboard/upload_video.html", context)

@user_passes_test(lambda u: u.is_staff)
def update_video(request):
    if request.method=="POST":
        video_id = request.POST.get('video')
        video = get_object_or_404(Lesson, id=video_id)
        form = AddLesson(request.POST, instance=video)
        if form.is_valid():
            form.save()
        return redirect("courses_admin")


@user_passes_test(lambda u: u.is_staff)
def add_branch(request):
    if request.method=="POST":
        form = AddBranch(request.POST)
        if form.is_valid():
            form.save()
            return redirect("branchs")
    else:
        form = AddBranch()
    context = {
        "title": "اضف فرع",
        "form":form,
    }
    return render(request, "dashboard/add_branch.html", context)


@user_passes_test(lambda u: u.is_staff)
def add_unit(request):
    if request.method == "POST":
        form = AddUnit(request.POST)
        if form.is_valid():
            form.save()
            return redirect("units")
    else:
        form = AddUnit()
    context = {
        "title": "اضف وحدة",
        "form": form,
    }
    return render(request, "dashboard/add_unit.html", context)


@user_passes_test(lambda u: u.is_staff)
def exams_admin(request):
    quizes=Quiz.objects.all()
    results = Result.objects.all()
    if request.method=="POST":
        quiz = Quiz.objects.get(id=request.POST.get("quiz_id"))
        quiz.delete()
    context = {
        "title": " الاختبارات",
        "quizes":quizes,
        "results": results
    }
    return render(request, "dashboard/exams_admin.html", context)


@user_passes_test(lambda u: u.is_staff)
def add_quiz(request):
    if request.method == "POST":
        form = QuizCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exams_admin")
    else:
        form=QuizCreationForm()
    context = {
        "title": " الاختبارات",
        "form":form,
    }
    return render(request, "dashboard/add_quiz.html", context)


@user_passes_test(lambda u: u.is_staff)
def update_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    form = QuizCreationForm(instance=quiz)
    if request.method=="POST":
        form = QuizCreationForm(request.POST or None, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect("courses_admin")
            
    context = {
        "form": form,
        "quiz":quiz,
    }
    return render(request, "dashboard/update_quiz.html", context)


@user_passes_test(lambda u: u.is_staff)
def add_question(request,id):
    AnswerFormSet = inlineformset_factory(Question, Answer, fields=("text", "correct"),extra=4)
    quiz=Quiz.objects.get(id=id)
    if request.method=="POST":
        formQu = QuestionCreationForm(request.POST)
        if formQu.is_valid():
            new_qu=formQu.save(commit=False)
            new_qu.quiz = quiz
            new_qu.save()
            formAnswer = AnswerFormSet(request.POST, instance=new_qu)
            if formAnswer.is_valid():
                formAnswer.save()
                formAnswer = AnswerFormSet()
                formQu = QuestionCreationForm()
    
    else:
        formAnswer = AnswerFormSet()
        formQu = QuestionCreationForm()
    
    context = {
        "title": " الاختبارات",
        "formAnswer": formAnswer,
        "formQu":formQu,
        "quiz":quiz,
    }
    return render(request, "dashboard/add_question.html", context)


@user_passes_test(lambda u: u.is_superuser)
def money(request):
    videos_active=RegisterVideo.objects.filter(active=True).order_by('-created')
    end_price=0
    startdate = date.today()
    enddate = startdate + timedelta(days=30)
    month = RegisterVideo.objects.filter(active=True, updated__range=[startdate, enddate])
    for i in month:
        end_price+=i.lesson.price
    if request.method=="POST":
        end_price = 0
        time=request.POST.get("month")
        month = RegisterVideo.objects.filter(active=True, updated__year=time.split("-")[0], updated__month=time.split("-")[1])
        for i in month:
            end_price+=i.lesson.price
    context = {
        "title": "ارباح المنصة",
        "videos_active":videos_active,
        "end_price":end_price,
    }
    return render(request, "dashboard/money.html", context)


@user_passes_test(lambda u: u.is_staff)
def subscriptions(request):
    lessons=RegisterVideo.objects.filter(active=True)
    courese=Branch.objects.all()
    if request.method=="POST":
        register = RegisterVideo.objects.get(
            id=request.POST.get("register_id"))
        register.delete()
    context = {
        "title": "جميع الاشتركات ",
        "lessons": lessons,
        "courese":courese,
    }
    return render(request, "dashboard/subscriptions.html",context)

@user_passes_test(lambda u: u.is_staff)
def watch(request):
    watches=Watched.objects.all()
    if request.method=="POST":
        get_watch=Watched.objects.get(id=request.POST.get("watch_id"))
        get_watch.counter = int(request.POST.get("watch_number"))
        get_watch.save()
    context = {
        "title": "جميع المشاهدة ",
        "watches": watches,
    }
    return render(request, "dashboard/watch.html",context)

"""
=================================
----------ajax functions---------
=================================
"""

@user_passes_test(lambda u: u.is_staff)
def ajax_load_year_branchs(request):
    year_id = request.GET.get('year_id')
    year = get_object_or_404(Year, id=year_id)
    branchs = Branch.objects.filter(year=year)
    context = {
        "branchs": branchs,
    }
    return render(request, "dashboard/ajax_load_year_branchs.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_year_units(request):
    year_id = request.GET.get('year_id')
    year = get_object_or_404(Year, id=year_id)
    units = Unit.objects.filter(branch__year=year)
    context = {
        "units": units,
    }
    return render(request, "dashboard/ajax_load_year_units.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_year_lessons(request):
    year_id = request.GET.get('year_id')
    year = get_object_or_404(Year, id=year_id)
    lessons = Lesson.objects.filter(unit__branch__year=year)
    context = {
        "lessons": lessons,
    }
    # return JsonResponse(list(lessons.values('id', 'name')), safe=False)
    return render(request, "dashboard/ajax_load_year_lessons.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_form_update_student(request):
    student_id = request.GET.get('student_id')
    user_id = request.GET.get('user_id')
    student = get_object_or_404(Student, id=student_id)
    user = get_object_or_404(User, id=user_id)
    form_student = UpdateStudentForm(instance=student)
    form_user=UpdateUserForm(instance=user)
    
    context = {
        "form_student": form_student,
        "form_user":form_user,
        "student_id":student_id,
        "user_id":user_id,
    }
    return render(request, "dashboard/ajax_load_form_update_student.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_form_update_video(request):
    video_id = request.GET.get('video_id')
    video = get_object_or_404(Lesson, id=video_id)
    form = AddLesson(instance=video)
    context = {
        "form": form,
        "video":video,
    }
    return render(request, "dashboard/ajax_load_form_update_video.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_form_update_unit(request):
    unit_id = request.GET.get('unit_id')
    unit = get_object_or_404(Unit, id=unit_id)
    form = AddUnit(instance=unit)
    context = {
        "form": form,
        "unit_id": unit_id,
    }
    return render(request, "dashboard/ajax_load_form_update_unit.html", context)


@user_passes_test(lambda u: u.is_staff)
def ajax_load_form_update_branch(request):
    branch_id = request.GET.get('branch_id')
    branch = get_object_or_404(Branch, id=branch_id)
    form = AddBranch(instance=branch)
    context = {
        "form": form,
        "branch_id": branch_id,
    }
    return render(request, "dashboard/ajax_load_form_update_branch.html", context)

"""
web hook

"""
@csrf_exempt
def status_video(request,token):
    token="a3df18b26a6444819db46ce800bb9b25"
    if request.method=="POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        lesson = get_object_or_404(Lesson, video_id=body_data['payload']['id'])
        lesson.ready=True
        lesson.save()
        
    return JsonResponse({'pk':1},safe=False)