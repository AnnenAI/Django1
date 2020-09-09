from django.urls import path,include
from .views import PostList,PostDetail,SearchList,AddPostView,UpdatePostView,DeletePostView

urlpatterns=[
    path('',PostList.as_view(),name='show_blog'),
    path('article/<slug:slug>',PostDetail.as_view(), name='show_post'),
    path('search/', SearchList.as_view(), name='search_results'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<slug:slug>', UpdatePostView.as_view(), name='edit_post'),
    path('article/<slug:slug>/remove', DeletePostView.as_view(), name='delete_post'),
]
