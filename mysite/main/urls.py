from django.urls import path, include
from .views import contact,AllPostListView,AllSearchListView, AllUsersView,FindUserView

urlpatterns = [
    path('',AllPostListView.as_view(),name='home'),
    path('search/',AllSearchListView.as_view(),name='search_results_all_posts'),
    path('users/',AllUsersView.as_view(),name='all_users'),
    path('users/search/',FindUserView.as_view(),name='find_user'),
    #path('contact/',contact,name='contact'),
]
