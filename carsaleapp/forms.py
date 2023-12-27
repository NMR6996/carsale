from django import forms
from .models import Comment, Contact
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"


class NewContactUs(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class EditUserProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
