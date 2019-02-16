from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from registration.models import Profile

class Registers(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',)

class ProfileForm(forms.ModelForm):
    """Форма для ввода номера телефона"""

    # "Изменяем название поля в форме"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefon'].label = 'Номер телефона без префикса "+"'

    def clean_telefon(self):
        "Проверяем поле с номером телефона"
        data = self.cleaned_data['telefon']
        p = Profile.objects.values('telefon')

        if {'telefon':data} in p:
            raise forms.ValidationError('такой номер существует')
        try:
            int(data)
        except ValueError:
            raise forms.ValidationError("Номер должен состоять из цифр!")  # в случае если номер состоит не из цифр
        if len(data) < 11:
            raise forms.ValidationError(
                "Номер должен состоять из 11 цифр (для Российской Федерации) или 12 (для Беларуси)")
        return data

    class Meta:
        model = Profile
        fields = ('telefon',)

class UserProfileRegistersForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = ('password1', 'password2',)


class UserProfileForm(forms.ModelForm):
    """Форма профия юзера для изменения номера телефона и фото аватарки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefon'].label = 'Номер телефона без префикса "+"!!!'
        self.fields['img'].label = 'Вставьте изображение'

    def clean_telefon(self):
        "Проверяем поле с номером телефона"

        data = self.cleaned_data['telefon']
        try:
            int(data)
        except ValueError:
            raise forms.ValidationError("Номер должен состоять из цифр!")  # в случае если номер состоит не из цифр
        if len(data) < 11:
            raise forms.ValidationError(
                "Номер должен состоять из 11 цифр (для Российской Федерации) или 12 (для Беларуси)")
        return data

    class Meta:
        model = Profile
        fields = ('telefon', 'img', )
