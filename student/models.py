from django.db import models
from django.contrib.auth.models import User
from edu.models import Year
from courses.models import Lesson,Branch
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName=models.CharField(max_length=50)
    ParentPhone=models.CharField(max_length=11)
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    address=models.CharField(max_length=150)
    device = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.fullName)

    @property
    def get_lesson_unactive(self):
        return self.student_video.filter(active=False).order_by('created')

    @property
    def get_lesson_active(self):
        return self.student_video.filter(active=True).order_by('created')

    @property
    def get_grade(self):
        grade=0
        for i in self.result_set.all().order_by('created'):
            grade+=i.degree
        return grade



class RegisterVideo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE ,related_name="student_video")
    lesson = models.ForeignKey(Branch, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.student} | {self.lesson} | {self.active}')

    @property
    def get_units(self):
        return self.lesson.get_units
    
    def get_lessons(self):
        return self.lesson.get_lessons


class OtpResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Watched(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_lesson")
    counter = models.IntegerField(default=1)
    def __str__(self):
        return str(self.student)
