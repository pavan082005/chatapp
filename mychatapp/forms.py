from django import forms
from django.forms import ModelForm
from mychatapp.models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Type your message here...',
                    'rows': 6,
                    'cols': 150,
                    'style': (
                        'resize: vertical;'
                        'border: 2px solid transparent;'
                        'border-image: linear-gradient(45deg, #007bff, #ff007b) 1;'
                        'box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'
                        'padding: 10px;'
                        'font-family: Arial, sans-serif;'
                        'font-size: 1rem;'
                        'color: #333;'
                        'background-color: #f9f9f9;'
                    )
                }
            )
        }
