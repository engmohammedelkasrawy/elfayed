from django import template
from django.shortcuts import  get_object_or_404
from student.models import Watched

register = template.Library()


@register.simple_tag
def get_watched(student,lesson):
    
    try:
        countered = Watched.objects.get(student=student, lesson=lesson).counter
        if countered >=2: 
            flag = "secondary"
        else:
            flag = "primary"
    except:
        countered = 0
        flag = "primary"

    return [countered, flag]
