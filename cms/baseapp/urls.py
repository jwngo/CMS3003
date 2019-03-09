from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('map/', views.incidents_map, name='map'),
    path('subscribe/', views.subscribe, name='subscribe'),

    # incidents related
    path('new_incident/', views.new_incident_form, name='new_incident_form'),
    path('incident_details/<int:incident_id>', views.incident_details, name='incident_details'),
    path('manage_incident/', views.manage_incident, name='manage_incident'),

    # report related
    path('new_report/', views.new_report_form, name='new_report_form'),
]