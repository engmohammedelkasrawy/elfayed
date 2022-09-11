from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from twilio.rest import Client
from exam.models import Quiz, Result
from .models import Student, RegisterVideo, OtpResetPassword,Watched
from .forms import UserCreationForm, StudentCreationForm
from .utils import random_digits

# Create your views here.
"""
=============================STUDENT=============================
FUNCTIONS (4):
    1 - profile()        | SHOW profile |
    2 - register_user()  | CREATE NEW USER AND STUDENT PROFILE |
    3 - login_user()     | LOGIN USER |
    4 - logout_user()    | LOGOUT USER |
================================================================
"""


@login_required
def profile(request):
    quizes = Quiz.objects.filter(year=request.user.student.year).order_by('created')
    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
        "quizes": quizes,

    }
    return render(request, "student/profile.html", context)


@login_required
def student_info(request):
    id_lesson = []
    for i in request.user.student.get_lesson_active:
        id_lesson.append(i.id)
    quizes = Quiz.objects.filter(lesson_id__in=id_lesson).order_by('created')

    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
        "quizes": quizes,
    }
    return render(request, "student/student_info.html", context)


@login_required
def off_videos(request):
    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
    }
    return render(request, "student/off_videos.html", context)


@login_required
def on_videos(request):
    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
    }
    return render(request, "student/on_videos.html", context)


@login_required
def quizzes(request):
    quizes = Quiz.objects.filter(
        year=request.user.student.year).order_by('created')
    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
        "quizes": quizes,
    }
    return render(request, "student/quizzes.html", context)


@login_required
def quiz_result(request):
    results = Result.objects.filter(student=request.user.student).order_by('created')
    context = {
        "title": f"الصفحة الشخصية | {request.user.student.fullName}",
        "results": results,
    }
    return render(request, "student/quiz_result.html", context)


def register_user(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == 'POST':
        studentForm = StudentCreationForm(request.POST)  # Student Model Form
        userForm = UserCreationForm(request.POST)  # User Model Form

        # Check if data in studentForm and userForm is valide
        if studentForm.is_valid() and userForm.is_valid():

            # Create User
            new_user = userForm.save(commit=False)
            # function to Hash Password
            new_user.set_password(userForm.cleaned_data['password1'])
            new_user.save()

            # Create Student
            new_student = studentForm.save(commit=False)
            new_student.user = new_user
            new_student.device = request.COOKIES.get('device')
            new_student.save()

            # Get User And Login
            user = authenticate(
                username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'],)
            login(request, user)
            return redirect('profile')

    else:
        studentForm = StudentCreationForm()
        userForm = UserCreationForm()

    context = {
        'title': 'تسجيل جديد',
        'studentForm': studentForm,
        'userForm': userForm,
    }
    return render(request, 'student/register_user.html', context)


def login_user(request, username=None, password=None):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # Check if user is exists and Check if COOKIES device in requset same that is in database
        if user is not None and user.student.device is None:
            new_user = user.student
            new_user.device = request.COOKIES.get('device')
            new_user.save()
            login(request, user)
            return redirect('register_videos')

        elif user is not None and user.student.device == request.COOKIES.get('device') and user.is_superuser == False and user.is_staff == False:
            login(request, user)
            return redirect('register_videos')

        
        elif user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('dashboard_index')
        
        else:
            messages.success(
                request, 'الهاتف او الرقم السري غير صحيح او قمت بفتح من جهاز اخر و متصفح اخر ')
    
    context = {
        'title': 'تسجيل الدخول',
    }
    return render(request, 'student/login_user.html', context)


def logout_user(request):
    logout(request)
    context = {
        'title': 'تسجيل الخروج',
    }
    return redirect('index')


def ask_reset_password(request):
    if request.method == "POST":
        get_user = get_object_or_404(
            User, username=request.POST.get("phoneNumber"))
        get, create = OtpResetPassword.objects.get_or_create(user=get_user)

        if not create:
            get.delete()
            new_otp = OtpResetPassword.objects.create(
                user=get_user, otp=random_digits(6))
            new_otp.save()
            account_sid = 'ACb3e013de8ef6a04e608d848dd0f5a0c8'
            auth_token = '20b9fbdbe4e5f43cd0c935b359186510'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'the code is {new_otp.otp}', from_='+12055259929', to=f'+2{request.POST.get("phoneNumber")}')
            return redirect("get_otp")
    context = {
        'title': 'تعين كلمة مرور',
    }
    return render(request, 'student/ask_reset_password.html', context)


def get_otp(request):
    if request.method == "POST":
        get_user = get_object_or_404(
            OtpResetPassword, otp=request.POST.get("otp"))

        return redirect(f"set_new_password/{request.POST.get('otp')}")
    context = {
        'title': 'تعين كلمة مرور',
    }
    return render(request, 'student/get_otp.html', context)


def set_new_password(request, otp):
    get_user = get_object_or_404(OtpResetPassword, otp=otp)
    if request.method == "POST":
        user = get_object_or_404(User, username=get_user.user)
        user.set_password(request.POST.get("pass"))
        user.save()
        get_user.delete()
        return redirect("login_user")
    context = {
        'title': 'تعين كلمة مرور',
    }
    return render(request, 'student/set_new_password.html', context)
