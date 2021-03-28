from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    phone = forms.CharField(max_length=255)
    class Meta:
        model = CustomUser
    def signup(self, request, user):
        user.phone = self.cleaned_data['phone']
        user.save()
        return user