#   sudo fuser -k 8000/tcp
from django.db import models
from django.contrib.auth.models import User

class SMSmess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages=models.TextField(max_length=70, blank=True, null=True, help_text='Текст может содержать 70 знаков')
    data=models.DateTimeField(auto_now_add=True, blank=True, null=True)
