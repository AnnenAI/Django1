from django.urls import path
from .views import (PostListView, PostDetailView,SearchListView,AddPostView,UpdatePostView,
DeletePostView, AddCategoryView,CategoriesListView,CategoryView,LikeView,AddCommentView)

urlpatterns=[
    path('users/<int:pk>',PostListView.as_view(),name='show_blog'),
    #path('article/<slug:slug>',PostDetailView.as_view(), name='show_post'),
    path('article/<slug:slug>',PostDetailView, name='show_post'),
    path('user/<int:pk>/search/', SearchListView.as_view(), name='search_results'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category/<str:category>/', CategoryView.as_view(), name='show_category'),
    path('categories/', CategoriesListView.as_view(), name='categories_list'),
    path('article/edit/<slug:slug>', UpdatePostView.as_view(), name='edit_post'),
    path('article/<slug:slug>/remove', DeletePostView.as_view(), name='delete_post'),
    path('like<slug:slug>',LikeView,name='like_post'),
]
