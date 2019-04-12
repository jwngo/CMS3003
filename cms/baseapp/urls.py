from django.urls import path, include
from django.contrib import admin
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', views.public_redirect, name='public'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.login_redirect, name='login_redirect'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/logout/', views.user_logout, name='user_logout'),
    path('map/', views.incidents_map, name='map'),
    path('subscribe/', views.subscribe, name='subscribe'),

    # incidents related
    path('new_incident/', views.new_incident_form, name='new_incident_form'),
    path('incident_details/<int:incident_id>', views.incident_details, name='incident_details'),
    path('manage_incident/', views.manage_incident, name='manage_incident'),

    # report related
    path('new_report/', views.new_report_form, name='new_report_form'),
]