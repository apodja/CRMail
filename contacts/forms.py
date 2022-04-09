from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from contacts.models import *
from bootstrap_modal_forms.forms import BSModalModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class ContactModelForm(BSModalModelForm):

    class Meta:

        model = Contact
        fields =['first_name','last_name','birthday','country','birthday','city','address','email', 'phone']


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields= '__all__'