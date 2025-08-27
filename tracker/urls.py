from django.urls import path
from . import views

urlpatterns = [
    path('patients/create/', views.PatientCreateView.as_view(),
         name='create a new patient'),
    path('patients/update-status/<pk>/',
         views.UpdatePatientStatusView.as_view(), name='update patient status'),
    path('doctors/list/', views.DoctorsListView.as_view(),
         name='doctors list'),

]
