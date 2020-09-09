from django import forms
from .models import Post

class AddForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','author','slug','body','date','picture')

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'author':forms.Select(attrs={'class':'form-control border border-primary'}),
            'slug':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'body':forms.Textarea(attrs={'class':'form-control border border-primary'}),
            'date':forms.DateTimeInput(attrs={'class':'form-control border border-primary'}),
            'picture':forms.FileInput(attrs={'class':'form-control-file py-2 border'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title','slug','body','date','picture')

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'slug':forms.TextInput(attrs={'class':'form-control border border-primary'}),
            'body':forms.Textarea(attrs={'class':'form-control border border-primary','rows':'30'}),
            'date':forms.DateTimeInput(attrs={'class':'form-control border border-primary'}),
            'picture':forms.FileInput(attrs={'class':'form-control-file py-2 border'}),
        }
