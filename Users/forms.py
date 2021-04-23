from allauth.account.forms import LoginForm
from django import forms
from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'name', 'gender', 'stu_id', 'department', 'remarks']
