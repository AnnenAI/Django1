from django.urls import path,include
from .views import PostList,PostDetail,SearchList,AddPostView,UpdatePostView

urlpatterns=[
    path('',PostList.as_view(),name='show_blog'),
    path('<slug:slug>',PostDetail.as_view(), name='show_post'),
    path('search/', SearchList.as_view(), name='search_results'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('edit/<slug:slug>', UpdatePostView.as_view(), name='edit_post'),
]
