from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from contacts.forms import CustomUserCreationForm, CustomUserChangeForm
from contacts.models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(Audience)
admin.site.register(EmailTemplate)
admin.site.register(Campaign)