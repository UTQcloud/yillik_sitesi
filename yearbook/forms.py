# yearbook/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Memory

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        # 'user' alanı hariç diğer tüm alanları forma dahil et
        exclude = ('user',)
        # Formdaki alanların daha güzel görünmesi için widget ekleyelim
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'future_specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_rotation': forms.TextInput(attrs={'class': 'form-control'}),
            'memorable_moment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'white_coat_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'your_choice_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Anınızı buraya yazın...'}),
        }