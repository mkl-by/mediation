from registration.views import register, profile_user, LogOutUser, LogInUser
from django.urls import path, re_path
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', register, name='reg'),
    path('profile_user', profile_user, name='profile_user'), #профайл
    #path('user/',  authViews.LoginView.as_view(template_name='users/user.html'), name='user'), #авторизуем
    #path('exit/',  authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'), #выходим
    path('exit/', LogOutUser.as_view(), name='exit'),
    path('user/',  LogInUser.as_view(), name='user'),
    #Смена пароля
    path('resetpassword/', authViews.PasswordResetView.as_view(template_name='users/resetssword.html'),
         name='resetpassword'),
    path('password_reset_confirm/<uidb64>/<token>/',
         authViews.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/done/',
         authViews.PasswordChangeDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_complete/',
         authViews.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    #re_path('exit/(?P<pk>[0-9]+)/', LogOutUser.as_view(), name='exit')
]
