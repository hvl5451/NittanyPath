"""NittanyPathApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', views.home, name="login-landing"),
    path('home/account/', views.account, name="account"),
    path('home/<str:course_id>/<int:sec_no>/', views.course, name="course"),
    path('home/<str:course_id>/<int:sec_no>/late_drop', views.late_drop, name="late_drop"),
    path('home/<str:course_id>/<int:sec_no>/Announcements/', views.announcements, name="announcements"),
    path('home/<str:course_id>/<int:sec_no>/Assignments/', views.assignments, name="assignments"),
    path('home/<str:course_id>/<int:sec_no>/Exams/', views.exams, name="exams"),
    path('home/<str:course_id>/<int:sec_no>/Grades/', views.grades, name="grades"),
    path('home/<str:course_id>/<int:sec_no>/Grade/<str:type>/<int:hw_no>', views.grade_assignment, name="grade_assignment"),
    path('home/<str:course_id>/<int:sec_no>/Discussion/', views.discussion, name="discussion"),
    path('home/<str:course_id>/<int:sec_no>/Discussion/<int:post_id>', views.post, name="post"),
]
