from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Quiz,Question,Result
from student.models import RegisterVideo
from courses.models import Lesson
# Create your views here.


@login_required
def quiz(request, id):
    exam=Quiz.objects.get(id=id)
    my_lesson = get_object_or_404(Lesson, id=exam.lesson.id)
    corse=get_object_or_404(RegisterVideo,lesson=my_lesson.unit.branch,student=request.user.student)
    if corse.active == False:
        return redirect("register_videos")
        
    context={
        "title":"امتحان",
        "exam":exam,
    }
    return render(request, "exam/quiz.html",context)


@login_required
def result(request):
    grade = 0
    user_Answer_mistakes = []
    user_Answer_true = []
    mistakesId = []
    
    if request.method=="POST":
        quiz = get_object_or_404(Quiz, id=request.POST.get('quiz_id'))
        for question in quiz.get_questions:
            for answer in question.get_answers:
                if answer.correct:
                    #questions_{question.id} value is answer id in template
                    if request.POST.get(f'questions_{question.id}') == str(answer.id):
                        grade += question.grade
                        user_Answer_true.append(question)
                    else:
                        mistakesId.append(question.id)
                        user_Answer_mistakes.append(
                            request.POST.get(f'questions_{question.id}'))

        question_mistakes = Question.objects.filter(id__in=mistakesId)
        mistakes = zip(list(question_mistakes), list(user_Answer_mistakes))
        get, create = Result.objects.get_or_create(student=request.user.student, quiz=quiz)
        
        if create:
            get.degree = grade
            get.save()
    
    else:
        return redirect('profile')
    
    context={
        "title":"امتحان",
        'mistakes': mistakes,
        'grade': grade,
        'quiz': quiz,
        'question_mistakes': question_mistakes,
        "user_Answer_true": len(user_Answer_true),
    }
    return render(request, "exam/result.html",context)