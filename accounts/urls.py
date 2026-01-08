from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.OnboardView.as_view(), name='sign up'),
    path('invite/doctor/', views.InviteDoctorView.as_view(),
         name='invite-doctor'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.MeView.as_view(), name='current user'),
]
