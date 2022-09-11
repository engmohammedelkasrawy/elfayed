from django.db import models
from edu.utils import slugify
from edu.models import Year
from .utils import video_directory_path

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=50)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    is_free = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.name} | {self.year}')


    @property
    def get_units(self):
        return self.unit_set.all().order_by('created')

    @property
    def get_lessons(self):
        qr=list()
        for unit in self.unit_set.all().order_by('created'):
            for lesson in unit.get_lessons:
                qr.append(lesson)
        return qr
    
    @property
    def get_count_student(self):
        return self.registervideo_set.filter(active=True)

class Unit(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.branch} | {self.name}')

    @property
    def get_lessons(self):
        return self.lesson_set.all().order_by('created')


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    video_id = models.CharField(max_length=150,blank=True, null=True)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    ready=models.BooleanField(default=False)
    private = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.unit} | {self.name}')

    @property
    def get_quiz(self):
        return self.quiz_set.all().order_by('created')

    def get_watch(self):
        return self.watched_set.all().order_by('created')

