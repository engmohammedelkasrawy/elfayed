from django import forms
from django.contrib.auth.models import User
from .models import Student
"""
=============================STUDENT=============================
FORMS (2) :
    1 - UserCreationForm()        | CREATE NEW USER FOMR |
    2 - StudentCreationForm()  | CREATE NEW STUDENT FOMR |
=================================================================
"""


class UserCreationForm(forms.ModelForm):
        
    username = forms.CharField(min_length=11, max_length=11,)
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username','password1', 'password2')

    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']

    def clean_username(self):
        numbers = ['010', '012', '011', '015', '۰۱۰', '۰۱۲', '۰۱۱', '۰۱٥']
        cd = self.cleaned_data
    
        if cd['username'][:3] not in numbers:
            raise forms.ValidationError('رقم غير صحيح تأكد ان يبداء الرقم با 010 او 012 او 011 او 015')
            
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الرقم.')
        
        if cd['username'].isnumeric() == False:
            raise forms.ValidationError('رقم غير صحيح')
            
        return cd['username']


class StudentCreationForm(UserCreationForm, forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ('fullName', 'ParentPhone', 'year', 'address',)

    def clean_fullName(self, *args, **kwargs):
        cd = self.cleaned_data
        # Loop in str(fullName) to check if in str a int
        for i in cd['fullName']:
            if i.isnumeric():
                raise forms.ValidationError('يجب الا يوجد ارقم في اسمك')
                break
        return cd['fullName']
        

    # def clean_username(self):
    #     cd = self.cleaned_data
    #     #check if Parent Phone same is student phone
    #     if cd['username'] == cd['ParentPhone']:
    #         raise forms.ValidationError('لا يجب ان يكون هاتف ولي الامر مطابق لهاتفك')
    #     return cd['ParentPhone']


class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('fullName', 'ParentPhone', 'year', 'address','device')


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)
