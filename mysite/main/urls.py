from django.urls import path, include
from .views import contact,AllPostListView,AllSearchListView

urlpatterns = [
    path('',AllPostListView.as_view(),name='home'),
    path('search/',AllSearchListView.as_view(),name='search_results_all_posts'),
    path('contact/',contact,name='contact'),
]
