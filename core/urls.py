from django.contrib import admin
from django.urls import path, include
from . import views
from core import views as core_views

urlpatterns = [

    # ---------------- HOME / BASIC PAGES ----------------
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('welcome/', views.welcome, name='welcome'),

    # ---------------- COACH / ATHLETE FEATURES ----------------
    path('injury/', views.submit_injury, name='injury'),
    path('coach-dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('recommend/', views.recommendations, name='recommendations'),
    path('injuryform/', views.InjuryReport, name='injuryform'),
    path('athletedashboard/', views.dashboard, name='athletedashboard'),
    path("logtraining/", views.log_training, name="logtraining"),
    # path('trainingload/', views.trainingload, name='trainingload'),

    # ---------------- STATIC PAGES ----------------
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ---------------- AUTH ----------------
    path('logout/', core_views.logout_user),

]