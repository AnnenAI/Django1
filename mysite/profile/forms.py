from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from blog.models import Profile
from django import forms

class SignUpForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control border border-primary'}))
    first_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control border border-primary'}))
    last_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control border border-primary'}))

    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self,*args,**kwards):
        super(SignUpForm,self).__init__(*args,**kwards)
        self.fields['username'].widget.attrs['class']='form-control border border-primary'
        self.fields['password1'].widget.attrs['class']='form-control border border-primary'
        self.fields['password2'].widget.attrs['class']='form-control border border-primary'

class AccountEditForm(UserChangeForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control border border-primary'}))
    first_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control border border-primary'}),required = False)
    last_name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control border border-primary'}),required = False)
    username=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control border border-primary'}))

    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('picture','bio','website_url','facebook_url','twitter_url','instagram_url')

        widgets = {
            'picture':forms.FileInput(attrs={'class':'form-control-file py-2 border'}),
            'bio':forms.Textarea(attrs={'rows': 20,'cols': 100,'class':'form  border-primary'}),
            'website_url':forms.URLInput(attrs={'class':'form-control border border-primary'}),
            'facebook_url':forms.URLInput(attrs={'class':'form-control border border-primary'}),
            'twitter_url':forms.URLInput(attrs={'class':'form-control border border-primary'}),
            'instagram_url':forms.URLInput(attrs={'class':'form-control border border-primary'}),
        }



class PasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border border-primary','type':'password'}))
    new_password1=forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control border border-primary','type':'password'}))
    new_password2=forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control border border-primary','type':'password'}))

    class Meta:
        model=User
        fields=('old_password','new_password1','new_password2')
