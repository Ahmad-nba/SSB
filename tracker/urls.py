from django.urls import path

from . import views

urlpatterns = [
    path('patients/create/', views.PatientCreateView.as_view(),
         name='create a new patient'),
    path('patients/list/', views.PatientListView.as_view(),
         name='list all patients'),
    path(
        "patients/update-status/<str:patient_code>/",
        views.UpdatePatientStatusView.as_view(),
        name="update-patient-status"
    ),
    path('patients/search/', views.PatientSearchView.as_view(),
         name='search-patient'),
    path('doctors/list/', views.DoctorsListView.as_view(),
         name='doctors list'),

]
