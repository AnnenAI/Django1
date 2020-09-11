from django import forms
from .models import Post, Category

class AddForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','author','category','slug','body','picture')

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'author':forms.Select(attrs={'class':'form-control border border-primary'}),
            'category':forms.Select(attrs={'class':'form-control border border-primary'}),
            'slug':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
            'picture':forms.FileInput(attrs={'class':'form-control-file py-2 border'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','category','slug','body','update_date','picture')

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'category':forms.Select(attrs={'class':'form-control border border-primary'}),
            'slug':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
            'update_date':forms.HiddenInput(),
            'picture':forms.FileInput(attrs={'class':'form-control-file py-2 border'}),
        }
