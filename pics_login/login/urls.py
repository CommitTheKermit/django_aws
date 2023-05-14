from django.urls import path
from login.views import LoginView, SignUpView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
]