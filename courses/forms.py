from django import forms
from .models import Branch,Unit,Lesson

class AddBranch(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name', 'year', 'price','is_free')


class AddUnit(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name', 'branch',)


class AddLesson(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'unit', 'private')
