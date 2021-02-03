from django.contrib import admin
from django.urls import path, include
from . import views

from .forms import LeakFormOne, LeakFormTwo, LeakFormThree, LeakFormFour

#/leaks
urlpatterns = [
    path('', views.instructions, name='instructions'),
    
    #get meter number
    path('meter_form', views.meter_number, name='meternumber'),
    
    #looping evidence form
    path('leak_evidence_form', views.leak_evidence_form, name='leakevidenceform'),
    path('move', views.move_files, name='move'),
    
    #checker templates
    path('check_one/', views.gatekeeper),
    path('filler/', views.filler),
    path('check_two/', views.gateKeeperTwo),
   
    #one template many forms
    path('forms/', views.LeakFormWizard.as_view([ LeakFormOne, LeakFormTwo, LeakFormThree, LeakFormFour])), 
    #many templates
    path('newForms/', views.LeakFormTemplatesWizard.as_view(views.FORMS)), 

    path('success/', views.submission_successful, name='submission_successful'),
]
