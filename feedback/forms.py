from django import forms
from feedback.models import SMSmess


class ChekSmsForm(forms.Form):
    """Форма для ввода проверочного номера"""
    number = forms.IntegerField(label='Проверочный код', min_value=1000, max_value=9999)

class SmsMessages(forms.ModelForm):
    class Meta:
        model = SMSmess
        fields = ('messages', )
