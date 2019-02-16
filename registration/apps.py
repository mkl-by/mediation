from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class RegistrationConfig(AppConfig):
    name = 'registration'
    verbose_name = _('profiles')  #не знаю зачем?

    def ready(self):
        #from registration.signals import post_save, create_profile
        import registration.signals   #регистрация сигнала, смотри еще __init__.py модуля default_app_config = 'registration.apps.RegistrationConfig'