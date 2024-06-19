from django import forms
from .models import Board

class BoaredFoorm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
        