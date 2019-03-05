from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('map/', views.map, name='map'),
    path('new_incident/', views.new_incident_form, name='new_incident_form'),
    path('incident_details/', views.incident_details, name='incident_details'),
]