from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfoModel(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email    = models.EmailField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class ProfileModel(models.Model):
    user      = models.OneToOneField(UserInfoModel, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50,  null=True, blank=True)
    email     = models.EmailField(max_length=50, null=True, blank=True)
    phone     = models.CharField(max_length=20,  null=True, blank=True)
    address   = models.TextField(null=True, blank=True)
    image     = models.ImageField(upload_to='media/profile', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name}'


class EducationModel(models.Model):
    user        = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='educations')  # ✅
    degree      = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)  
    start_year  = models.PositiveIntegerField(null=True, blank=True)
    end_year    = models.PositiveIntegerField(null=True, blank=True)
    result      = models.CharField(max_length=50, null=True, blank=True)    

    def __str__(self):
        return f'{self.degree}-{self.institution}'


class ExperienceModel(models.Model):
    user         = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='experiences')  # ✅
    company_name = models.CharField(max_length=100, null=True, blank=True) 
    role         = models.CharField(max_length=50,  null=True, blank=True)  
    start_date   = models.DateField(null=True, blank=True)
    end_date     = models.DateField(null=True, blank=True)
    description  = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.company_name}-{self.role}'


class SkillModel(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert',       'Expert'),
    ]
    user        = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='skills')
    skill_name  = models.CharField(max_length=100, null=True, blank=True)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Beginner')

    def __str__(self):
        return f'{self.skill_name}-{self.proficiency}'


class ProjectModel(models.Model):
    user         = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200, null=True, blank=True)
    description  = models.TextField(null=True, blank=True)
    link         = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.project_name}'


class ResumeModel(models.Model):
    TEMPLATE_TYPE = [
        ('classic', 'Classic'),
        ('modern',  'Modern'),
        ('minimal', 'Minimal'),
    ]
    user            = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='resumes')  # ✅
    title           = models.CharField(max_length=200, null=True, blank=True)
    template_choice = models.CharField(max_length=20, choices=TEMPLATE_TYPE, default='classic')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'


class ResumeSectionModel(models.Model):
    resume     = models.OneToOneField(ResumeModel, on_delete=models.CASCADE, related_name='section')
    education  = models.ManyToManyField(EducationModel,  blank=True)
    experience = models.ManyToManyField(ExperienceModel, blank=True)
    skills     = models.ManyToManyField(SkillModel,      blank=True)
    projects   = models.ManyToManyField(ProjectModel,    blank=True)

    def __str__(self):
        return f'{self.resume.title}'