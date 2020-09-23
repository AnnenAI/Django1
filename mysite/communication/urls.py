from django.urls import path
from .views import MessagesView,DialogueView

urlpatterns=[
    path('',DialogueView.as_view(), name='dialogue'),
    path('<int:pk>/',MessagesView.as_view(), name='messages'),
]
