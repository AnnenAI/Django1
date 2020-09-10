from django.urls import path
from .views import PostListView,PostDetailView,SearchListView,AddPostView,UpdatePostView,DeletePostView

urlpatterns=[
    path('',PostListView.as_view(),name='show_blog'),
    path('article/<slug:slug>',PostDetailView.as_view(), name='show_post'),
    path('search/', SearchListView.as_view(), name='search_results'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<slug:slug>', UpdatePostView.as_view(), name='edit_post'),
    path('article/<slug:slug>/remove', DeletePostView.as_view(), name='delete_post'),
]
