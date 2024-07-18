from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactSubmission

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user
    
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['email', 'message']


