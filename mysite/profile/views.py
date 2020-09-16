from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from blog.models import Profile, User
from django.db.models.signals import post_save
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .forms import SignUpForm,PasswordChangeForm,ProfileEditForm,AccountEditForm

def SettingsView(request):
    template_name='registration/settings.html'
    context={
        'nbar':'settings'
    }
    return render(request,template_name,context)

class ProfileEditView(generic.UpdateView):
    model=Profile
    form_class=ProfileEditForm
    template_name='registration/edit-profile.html'
    success_url=reverse_lazy('home')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self,*args,**kwards):
        context=super(ProfileEditView,self).get_context_data(*args,**kwards)
        context['nbar']='settings'
        context['nbarp']='profile'
        return context

class AccountEditView(generic.UpdateView):
    form_class=AccountEditForm
    template_name='registration/edit-account.html'
    success_url=reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def get_context_data(self,*args,**kwards):
        context=super(AccountEditView,self).get_context_data(*args,**kwards)
        context['nbar']='settings'
        context['nbarp']='account'
        return context

class ShowProfilePageView(generic.DetailView):
    model=Profile
    template_name='registration/profile.html'

    def get_context_data(self,*args,**kwards):
        user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context=super(ShowProfilePageView,self).get_context_data(*args,**kwards)
        context['nbar']='profile'
        context['page_user']=user
        return context

class PasswordChangeView(PasswordChangeView):
    form_class=PasswordChangeForm
    template_name='registration/change-password.html'
    success_url=reverse_lazy('home')

    def get_context_data(self,*args,**kwards):
        context=super(PasswordChangeView,self).get_context_data(*args,**kwards)
        context['nbar']='edit_profile'
        return context

class UserRegisterView(generic.CreateView):
    form_class=SignUpForm
    template_name='registration/register.html'
    success_url=reverse_lazy('login')

    def get_context_data(self,*args,**kwards):
        context=super(UserRegisterView,self).get_context_data(*args,**kwards)
        context['nbar']='register'
        return context

def createUserProfile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)

post_save.connect(createUserProfile, sender=User)
