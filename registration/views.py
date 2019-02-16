from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.shortcuts import resolve_url
from registration.form import Registers, ProfileForm, UserProfileRegistersForm, UserProfileForm
from registration.models import Profile

#
def register(request):
    """регистрация пользователя"""
    if request.method=='POST':
        form=Registers(request.POST)
        form_profile=ProfileForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             password=form.cleaned_data.get('password1')
             tlf=form_profile.cleaned_data.get('telefon')
#регистрируемся
             user = authenticate(username=username, password=password)
             login(request, user)
# Заменяем дефолтный номер на новый
             profile_obj = Profile.objects.get(user_id=request.user.id)
             profile_obj.telefon = tlf
             profile_obj.save()
             return redirect('sms_control')
    else:
        form=Registers()
        form_profile=ProfileForm()
    return render(request, 'users/registration.html', {'form': form, 'form_profile': form_profile})
@login_required
def profile_user(request):
    """изменение профиля пользователя"""
    if request.method=='POST':
        prof_user = UserProfileRegistersForm(request.POST, instance=request.user)
        prof_user_tlf_img = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_user.is_valid() and prof_user_tlf_img.is_valid():
            prof_user_tlf_img.save()
            prof_user.save()
            pos=Profile.objects.get(user_id=request.user.id)
            if  pos.activ_user == True:
                messages.success(request, f'Данные пользователя успешно изменены')
                return redirect('profile_user')
            else:
                return redirect('sms_control')
    else:
        prof_user=UserProfileRegistersForm(instance=request.user)
        prof_user_tlf_img=UserProfileForm(instance=request.user.profile)
    contex={'prof_user': prof_user, 'prof_user_tlf_img': prof_user_tlf_img}
    return render(request,'users/profile_user.html', contex)
#при выходе с сайта сохраняем дату выхода
class LogOutUser(LogoutView):
    template_name = 'users/exit.html'
    def dispatch(self, request, *args, **kwargs):
        pos=Profile.objects.get(user_id=request.user.id)
        pos.date_exit=timezone.now()      #сохраняем дату выхода
        pos.save()
        return super().dispatch(request, *args, **kwargs)
#при входе пользователя проверяем разницу даты выхода и входа
class LogInUser(LoginView):
    template_name = 'users/user.html'
    def get_success_url(self):
        url = self.get_redirect_url()
        date_login=timezone.now()
        pos=Profile.objects.get(user_id=self.request.user.id)
        delta=date_login.day-pos.date_exit.day #проверяем сколько прошло времени после выхода пользователя
        if delta: #если дельта !=0, то
            pos.done_sum_sms=0
            pos.activ_sms=True
            pos.save()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)












