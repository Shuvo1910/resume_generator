from django.urls import path
from .views import *

urlpatterns = [
    # Auth & Home
    path('', home_page, name='home_page'),
    path('login/', login_page, name='login_page'), 
    path('register/', register_page, name='register_page'),
    path('logout/', logout_page, name='logout_page'),
    path('update_pwd/', change_password, name='change_password'),
    
    # Dashboard & Profile
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('profile/', profile_page, name='profile_page'),
    path('update_profile/', update_profile, name='update_profile'), 
    
    # Data Entry (The Pool of Data)
    path('add-education/', add_education, name='add_education'),
    path('add-experience/', add_experience, name='add_experience'),
    path('add-skill/', add_skill, name='add_skill'),
    path('add-project/', add_project, name='add_project'), 
    
    # Resume Builder (The Generation Process)
    path('create-resume/', create_resume, name='create_resume'),
    path('select-sections/<int:resume_id>/', select_sections, name='select_sections'),
    path('resume-view/<int:resume_id>/', resume_view, name='resume_view'),
]
