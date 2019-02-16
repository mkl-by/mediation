from django.contrib.auth.models import User
from registration.models import Profile
from django.db.models.signals import post_save  # функция срабатывает когда изменяется User
from django.dispatch import receiver  # получатель


@receiver(post_save, sender=User)  # когда добавляем в User вызывается post_save
def create_profile(sender, instance, created,
                   **kwargs):  # sender таблица из которой получаем данные, instance объект который создается
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)  # когда добавляем в User вызывается post_save
def save_profile(sender, instance,
                 **kwargs):  # sender таблица из которой получаем данные, instance объект который создается
    """обновление данных пользователя"""
    instance.profile.save()
# для того чтобы это заработало необходимо зайти  в apps.py и импортировать модуль def ready(self): import users.signals

# post_save.connect(create_profile, sender=User)
