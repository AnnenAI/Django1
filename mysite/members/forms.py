from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
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
