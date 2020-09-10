from django.urls import path, include
from .views import contact, index

urlpatterns = [
    path('',index,name='index'),
    path('contact/',contact,name='contact'),
]
