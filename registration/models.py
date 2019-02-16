from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.contrib import admin
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=12, default='375447085046')
    img = models.ImageField(default='default.jpg', upload_to='user_images')
    activ_user=models.BooleanField(default=False)
#модель для ограничения колличества отправленных смс
    activ_sms=models.BooleanField(default=True)          #запрет на отправку sms
    done_sum_sms=models.IntegerField(default=0)          #колличество отправленных смс в течении 24 часов
    data_input_end_sms=models.TextField(max_length=150, blank=True, null=True)
    date_exit=models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    class Meta:
        ordering=['date_exit']
        def __init__(self):
            return ('%d-%m-%Y'.format(self.date_exit))
    # def __str__(self):
    #     return f'Профайл пользователя {self.user.username}, номер телефона {self.telefon}, Зарегистрирован={self.activ_user}, ' \
    #         f'дата выхода {self.date_exit}'

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

class AdminProfile(admin.ModelAdmin):

    list_display = ['user',
                    'telefon',
                    'img',
                    'activ_user',
                    'activ_sms',
                    'done_sum_sms',
                    'data_input_end_sms'
                  , ]