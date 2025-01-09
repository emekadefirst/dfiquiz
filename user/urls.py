from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="Login route"),
    path("<str:pk>/", views.UserRetrieveUpdateDestroyView.as_view(), name="details"),
    path("v1/users/", views.UserCreateView.as_view(), name="All user routes"),
    path("v1/register/", views.UserCreateView.as_view(), name="Signup route"),
]
