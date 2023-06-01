from django.urls import path
from login.views import LoginView, SignUpView, FindIdView, FindPwView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('findid', FindIdView.as_view()),
    path('findpw', FindPwView.as_view()),
]