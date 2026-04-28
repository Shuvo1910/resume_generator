from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from resume.models import *
from django.contrib.auth.forms import PasswordChangeForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = UserInfoModel
        fields = [
            'username',
            'email',
        ]

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = [
            'full_name',
            'email',
            'phone',
            'address',
            'image',
        ]

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
            
class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        fields = ['degree', 'institution', 'start_year', 'end_year', 'result']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values(): 
            field.widget.attrs.update({'class': 'form-control'})


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceModel
        fields = ['company_name', 'role', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values(): 
            field.widget.attrs.update({'class': 'form-control'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = SkillModel
        fields = ['skill_name', 'proficiency']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values(): 
            field.widget.attrs.update({'class': 'form-control'})
        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['project_name', 'description', 'link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

class ResumeForm(forms.ModelForm):
    class Meta:
        model  = ResumeModel
        fields = ['title', 'template_choice']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

class ResumeSectionForm(forms.ModelForm):
    class Meta:
        model   = ResumeSectionModel
        fields  = ['education', 'experience', 'skills', 'projects']
        widgets = {
            'education' : forms.CheckboxSelectMultiple(),
            'experience': forms.CheckboxSelectMultiple(),
            'skills'    : forms.CheckboxSelectMultiple(),
            'projects'  : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):   
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['education'].queryset  = EducationModel.objects.filter(user=user)
            self.fields['experience'].queryset = ExperienceModel.objects.filter(user=user)
            self.fields['skills'].queryset     = SkillModel.objects.filter(user=user)
            self.fields['projects'].queryset   = ProjectModel.objects.filter(user=user)