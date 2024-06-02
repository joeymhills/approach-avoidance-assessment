from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_participant, name='register_participant'),
    path('success/<str:subject_id>/', views.participant_success, name='participant_success'),
    path('manage/', views.manage_participants, name='manage_participants'),
    path('detail/<int:participant_id>/', views.participant_detail, name='participant_detail'),
    path('edit/<int:participant_id>/', views.edit_participant, name='edit_participant'),
    path('delete/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('start-experiment/<int:participant_id>/', views.start_experiment, name='start_experiment'),
    path('run-trial/', views.run_trial, name='run_trial'),
    path('save-response/', views.save_response, name='save_response'),
    path('experiment-complete/', views.experiment_complete, name='experiment_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]