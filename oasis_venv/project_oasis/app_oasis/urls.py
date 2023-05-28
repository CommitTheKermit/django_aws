from django.urls import path
from app_oasis.views import LoginView, SignUpView, FindEmailView, FindPwView, EmailSendView, EmailVerifyView, CafeInfoView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('signup/<int:bid>/', SignUpView.as_view()),
    path('findemail', FindEmailView.as_view()),
    path('findpw', FindPwView.as_view()),
    path('mailsend', EmailSendView.as_view()),
    path('mailverify',EmailVerifyView.as_view()),
    path('cafeinfo', CafeInfoView.as_view())
]