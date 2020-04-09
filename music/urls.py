from django.urls import path,re_path
from django.conf.urls import url, include
from allauth.account.views import email_verification_sent
# from allauth.account.views import ConfirmEmailView
from .views import ListCreateSongsView, LoginView, RegisterUserView, SongsDetailView,null_view, complete_view,ConfirmEmailView

urlpatterns = [
    path('songs/', ListCreateSongsView.as_view(), name="songs-list-create"),
    path('songs/<int:pk>/',SongsDetailView.as_view(),name="songs-detail"),
    path('auth/login/',LoginView.as_view(),name="auth-login"),
    re_path('auth/register/account-email-verification-sent/',email_verification_sent,name="account_email_verification_sent"),
    re_path('auth/account-confirm-email/(?P<key>[-:\w]+)/',ConfirmEmailView.as_view(),name="account_confirm_email"),
    re_path('auth/register/complete/', complete_view, name='account_confirm_complete'),
    re_path('', include('rest_auth.urls')),
    path('auth/register/',include('rest_auth.registration.urls'))
]
