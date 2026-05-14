from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

def home_page(request):
    return render(request, 'home.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            user = form_data.save()
            login(request, user) 
            messages.success(request, f'Registration successful! Welcome, {user.username}.')
            return redirect('home_page')
        
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form_data = RegisterForm()

    context = {
        'form_data': form_data
    }
    return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
        
    if request.method == 'POST':
        form_data = LoginForm(request, data=request.POST)   
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid username or password.')  


    form_data = LoginForm()
    
    context = {
        'form_data': form_data
    }

    return render(request, 'login.html', context)


@login_required
def logout_page(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login_page')


@login_required
def profile_page(request):
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except:
        profile = None

    if request.method == 'POST':
        form_data = ProfileForm(request.POST, request.FILES, instance = profile)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user 
            data.save()
            return redirect('profile_page')
    form_data = ProfileForm(instance = profile)

    context = {
        'form_data': form_data,
        'form_title': 'Update User Profile Info',
        'btn_name': 'Update Profile'
    }
    return render(request, 'master/base-form.html',context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form_data = MyPasswordChangeForm(request.user, request.POST)
        if form_data.is_valid():
            user = form_data.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated!')
            return redirect('profile_page') 
        else:
            messages.error(request, 'Check the mistakes!')

    form_data = MyPasswordChangeForm(request.user)
    
    context = {
        'form_data': form_data,
        'form_title': 'Change Password',
        'btn_name': 'Update Password'
    }
    return render(request, 'master/base-form.html', context) 


@login_required
def add_education(request):
    if request.method == 'POST':
        form_data = EducationForm(request.POST)
        if form_data.is_valid():
            obj = form_data.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Education added!")
            return redirect('profile_page')
    
    context = {
        'form_data': EducationForm(), 
        'form_title': 'Add Education', 
        'btn_name': 'Add to Profile'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def add_skill(request):
    if request.method == 'POST':
        form_data = SkillForm(request.POST)
        if form_data.is_valid():
            obj = form_data.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('profile_page')
    
    context = {
        'form_data': SkillForm(), 
        'form_title': 'Add Skill', 
        'btn_name': 'Add to Profile'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('profile_page')
    context = {
        'form_data': ExperienceForm(), 
        'form_title': 'Add Experience', 
        'btn_name': 'Add to Profile'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def add_project(request):
    if request.method == 'POST':
        form_data = ProjectForm(request.POST)
        if form_data.is_valid():
            project = form_data.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('profile_page')
    else:
        form_data = ProjectForm()

    context = {
        'form_data': form_data,
        'form_title': 'Add Project',
        'btn_name': 'Add to Profile'
    }
    return render(request, 'master/base-form.html', context)



@login_required
def dashboard_page(request):
    resumes = ResumeModel.objects.filter(user=request.user)
    context = {
        'resumes': resumes, 
        'resume_count': resumes.count()
    }
    return render(request, 'dashboard.html', context)


@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('select_sections', resume_id=resume.id)
    context = {
        'form_data': ResumeForm(), 
        'form_title': 'Create New Resume', 
        'btn_name': 'Next: Select Sections'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def select_sections(request, resume_id):
    resume = get_object_or_404(ResumeModel, id=resume_id, user=request.user)
    try:
        section_instance = resume.section
    except ResumeSectionModel.DoesNotExist:
        section_instance = None

    if request.method == 'POST':
        form = ResumeSectionForm(request.POST, instance=section_instance, user=request.user)
        if form.is_valid():
            section = form.save(commit=False)
            section.resume = resume
            section.save()
            form.save_m2m() 
            messages.success(request, "Resume generated successfully!")
            return redirect('dashboard_page')
    
    context = {
        'form_data': ResumeSectionForm(instance=section_instance, user=request.user),
        'form_title': f'Select Sections for: {resume.title}',
        'btn_name': 'Finish Resume'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def resume_view(request, resume_id):
    resume = get_object_or_404(ResumeModel, id=resume_id, user=request.user)
    return render(request, 'resume_view.html', {'resume': resume})
