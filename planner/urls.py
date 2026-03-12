from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('preferences/', views.user_preferences, name='preferences'),
    path('activities/', views.activity_selection, name='activities'),
    path('timetable/', views.final_timetable, name='timetable'),
    path('logout/', views.user_logout, name='logout'),
    path('export-ics/', views.export_ics, name='export_ics'),
    path('save-progress/', views.save_progress, name='save_progress'),
]
