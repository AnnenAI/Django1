from django import forms
from .models import Message

class SendMessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields = ('text',)

        widgets = {
            'text':forms.Textarea(attrs={'rows': 10,'cols': 80,'class':'form  border-primary'}),
        }
