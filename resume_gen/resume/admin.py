from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UserInfoModel, 
    ProfileModel, 
    EducationModel, 
    ExperienceModel, 
    SkillModel, 
    ProjectModel,
    ResumeModel,        
    ResumeSectionModel  
)

@admin.register(UserInfoModel)
class UserInfoAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'email', 'phone')
    search_fields = ('full_name', 'user__username', 'email')

@admin.register(EducationModel)
class EducationAdmin(admin.ModelAdmin):
    # FIXED: changed 'instituate' to 'institution'
    list_display = ('degree', 'institution', 'user', 'start_year', 'end_year', 'result')
    list_filter = ('start_year', 'end_year', 'degree')
    search_fields = ('institution', 'degree', 'user__username')

@admin.register(ExperienceModel)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'user', 'start_date', 'end_date')
    list_filter = ('company_name', 'role')
    search_fields = ('company_name', 'role', 'user__username')

@admin.register(SkillModel)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'proficiency', 'user')
    list_filter = ('proficiency',)
    search_fields = ('skill_name', 'user__username')

@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'link')
    search_fields = ('project_name', 'user__username')

# Added registration for Resume models so you can see them in admin
@admin.register(ResumeModel)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template_choice', 'created_at')

@admin.register(ResumeSectionModel)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ('resume',)
