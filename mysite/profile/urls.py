from django.urls import path
from .views import UserRegisterView,PasswordChangeView,ShowProfilePageView,ProfileEditView,AccountEditView,SettingsView
#from django.contrib.auth import views as auth_views


urlpatterns=[
    path('register/',UserRegisterView.as_view(),name='register'),
    path('<int:pk>/',ShowProfilePageView.as_view(),name='profile'),
    path('settings/',SettingsView,name='settings'),
    path('settings/edit-account/',ProfileEditView.as_view(),name='edit_profile'),
    path('settings/edit-profile/',AccountEditView.as_view(),name='edit_account'),
    path('settings/password/',PasswordChangeView.as_view()),
]
