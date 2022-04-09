from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Audience(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) :
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=255,blank=True , null=True)
    last_name = models.CharField(max_length=255,blank=True , null=True)
    phone = models.CharField(max_length=255,blank=True , null=True)
    email = models.EmailField(max_length=255,blank=True , null=True)
    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255,blank=True , null=True)
    country = models.CharField(max_length=255,blank=True , null=True)
    address = models.CharField(max_length=255,blank=True , null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

    def __str__(self) :
        return self.first_name+self.last_name

class EmailTemplate(models.Model):
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.path

STATUS_CHOICES = (
        ("ONGOING", "Ongoing"),
        ("STOPPED", "Stopped"),
        ("DRAFT", "Draft")
        )

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    frm = models.EmailField(max_length=255, null=True)
    subject = models.CharField(max_length=255)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    audience = models.ForeignKey(Audience, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="DRAFT")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


 