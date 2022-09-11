from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Branch,Lesson
from student.models import RegisterVideo, Watched
import json
import requests
from requests_toolbelt import MultipartEncoder
from django.contrib import messages
# Create your views here.
"""
=============================COURSES=============================
FUNCTIONS (4):
    1 - register_videos():
            GET ALL LESSONS FILTER BY YEAR STUDENT AND REGISTER IT 
    2 - lesson():          
            GET LESSON AND CHECK IF LESSON ACTIVE 
            OR NOT IF ONT ACTIVE REDERICT PROFILE 
================================================================
"""

@login_required
def register_videos(request):
    #GET branchs from database and filter by year student
    branchs=Branch.objects.filter(year=request.user.student.year).order_by('created')
    if request.method == "POST":
        #if lesson in student register not do anything if not in create video register not active
        branch = get_object_or_404(Branch, id=request.POST.get("branch_id"))
        if branch.is_free:
            get, register = RegisterVideo.objects.get_or_create(student=request.user.student, lesson=branch,active=True)
            return redirect("on_videos")
        else:
            get, register = RegisterVideo.objects.get_or_create(student=request.user.student, lesson=branch)
            return redirect("off_videos")
    context = {
        "title": "منصة الفايد",
        "branchs":branchs,
    }
    return render(request, "courses/register_videos.html",context)


@login_required
def lesson(request, branch_id, lesson_id):
    branch = get_object_or_404(RegisterVideo, id=branch_id, student=request.user.student)
    active = Lesson.objects.filter(unit__in=branch.get_units).order_by('created')
    my_lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if branch.active == False and my_lesson not in branch.get_lessons:
        return redirect('off_videos')
    else:
        url = f"https://dev.vdocipher.com/api/videos/{my_lesson.video_id}/otp"
        payload = json.dumps({
            "annotate": json.dumps([
                {'type': 'rtext', 'text': f'{request.user.username}', 'alpha': '0.60',
                    'color': '0xFF0000', 'size': '20', 'interval': '5000'}
            ])
        })
        headers = {
            'Authorization': "Apisecret DzJNvBi24Htggyg5HpvDPpex6YAKIgbMNaRbPV5mImVUCM1ds3WMUR9PpcGM1wd6",
            'Content-Type': "application/json",
            'Accept': "application/json"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        get, create = Watched.objects.get_or_create(
            student=request.user.student, lesson=my_lesson)
        
        if create == False and get.counter != 2:
            get.counter+=1
            get.save()
        
        if get.counter > 2  and request.user.is_superuser ==False:
            messages.success(request, 'انتهت مشاهدتك لهذا الدرس')
            return redirect('on_videos')


        obj = json.loads(response.text)
    context = {
        "title": "الفايد",
        "branch":branch,
        'active':active,
        "otp": obj['otp'],
        "playbackInfo":obj['playbackInfo'],
        "my_lesson":my_lesson,
        
    }
    return render(request, "courses/lesson.html",context)


    