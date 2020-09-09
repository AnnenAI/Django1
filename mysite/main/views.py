from django.shortcuts import render

def index(request):
    return  render(request,'main/home.html',)

def contact(request):
    context={'info':{'My Email':'leksey0002@gmail.com','My phone':'380xxxxxxxxx'}}
    return  render(request,'main/basic.html',context)
