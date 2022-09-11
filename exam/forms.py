from django import forms
from .models import Quiz, Question


class QuizCreationForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("title" , "description" ,"year" ,"lesson" , )


class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("text" , "grade" ,)