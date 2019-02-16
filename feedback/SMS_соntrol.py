import random, requests, datetime
from django.shortcuts import render, redirect
from feedback.forms import ChekSmsForm, SmsMessages
from django.contrib.auth.models import User
from registration.models import Profile
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def sms_code():
   # code_sms = 1111 # аля тест
    code_sms = random.randint(1000, 9999)
    return str(code_sms)

def mess_deactivation(request, datt):
    # выводим время оставшееся до конца блокировки
    t = datetime.datetime.strptime(datt, '%Y-%m-%d %H:%M:%S.%f')
    messages.error(request, f'Отправлено 3 смс, время окончания блокировки {(t.day + 1):02}-{t.month:02}-{t.year} в {t.hour}:{t.minute:02}.')

class SMS_valid(View):
    def get(self, request, *args, **kwargs):
        pos = Profile.objects.get(user_id=request.user.id)
        tel = pos.telefon
        mess = 'Медиация: код регистрации'
        self.sms(request, mess, tel)
        if pos.activ_sms:
            messages.success(request, 'На ваш номер направлено сообщение с кодом регистрации')
            sms_form = ChekSmsForm()
            print(request.session['sms_error'])
            return render(request, 'feedback/smscont.html', {'sms_form': sms_form, 'sms_error': request.session['sms_error']})
        else:
            mess_deactivation(request, pos.data_input_end_sms)
            return redirect('home')

    def post(self, request, *args, **kwargs):
#юзер ввел код
        sms_form = ChekSmsForm(request.POST)
        if sms_form.is_valid():
            number=sms_form.cleaned_data.get('number')
            try:
                if number==int(request.session['code_sms']):
#если номер верен ставим тру для астiv_user
                    pos=Profile.objects.get(user_id=request.user.id)
                    pos.activ_user=True
                    pos.save()
                    messages.success(request, f'пользователь {pos.user.username} успешно создан')
                else:
                    try:
                        messages.error(request, f'Вы не прошли проверку sms кодом и не сможете отправлять сообщение '
                        f'медиатору. Повторите регистрацию')
                        #request.session.clear()
                        return redirect('profile_user')
                    except KeyError:
                        pass
            except KeyError:
                pass
            return redirect('home')

    def sms(self, request, message, tel):
        # если пользователь не активен считаем сколько осталось времени для разрешения повторной активации через sms
        pos = Profile.objects.get(user_id=request.user.id)
        activsms=pos.activ_sms
        if not activsms:
            date=pos.data_input_end_sms
            if (datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')).days >= 1:
                print((datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')).days)
                pos.activ_sms=True
                pos.done_sum_sms=0
                pos.save()

        #данные отсылаемые на  сервер для связи с юзером
        if pos.activ_sms:
            number = str(sms_code()).upper()
            request.session['code_sms']=number
            url_onesms = 'http://app.sms.by/api/v1/sendQuickSms'
            token = '15ec7b40b80cc6ca32433f1cbb000513'
            mess=('Медиация: код регистрации '+number if message=='Медиация: код регистрации' else message)
            one_sms = {
            'token': token,
            'message': mess,
            'phone': tel,
            }
    #       req = requests.get(url_onesms, params=one_sms)  # отправляем сообщение юзеру
            # response = req.json()
            print(number)
            response={'asdfsdf':'sdfsdfsd'} #cлужит для теста, отключение отправки смс на сервер

            # ошибки сервера отправки сообщений
            err = {'incorrect phone number': 'Неправильный номер телефона',
               'incorrect arguments': 'Ошибка в количестве или типах параметров',
               'billing error': 'Ошибка биллинга (например у пользователя нет API тарифного плана',
               'message_id not found': 'Рассылка не найдена',
               'access denied': 'Рассылка не подтверждена администратором',
               'limit exceeded': 'Исчерпан лимит отправляемых сообщений в пределах тарифа',
               'undefined error': 'Ошибка приложения'
               }
            #провереяем наличие ошибок
            for keey, vall in response.items():
                if keey=='error':
                    for key, value in err.items():
                        if vall==key:
                            request.session['sms_error']=value
                else:
                    request.session['sms_error']=False

            #считаем если колличество отправок сообщений равно 3
            pos.done_sum_sms +=1
            pos.save()
            print(pos.done_sum_sms)
            if pos.done_sum_sms == 3:
                pos.data_input_end_sms = str(datetime.datetime.now())
                pos.activ_sms=False
                pos.save()
        return

class Sms_mediation(SMS_valid):

    def get(self, request, *args, **kwargs):
        pos = Profile.objects.get(user_id=request.user.id)
        if pos.activ_user & pos.activ_sms:
            form_mess=SmsMessages()
        else:
            mess_deactivation(request, pos.data_input_end_sms)
            return redirect('home')
        return render(request, 'feedback/smsmes.html', {'form_mess': form_mess})

    def post(self, request, *args, **kwargs):
        form_mess=SmsMessages(request.POST)
        pos = Profile.objects.get(user_id=request.user.id)
        if pos.activ_user & form_mess.is_valid() & pos.activ_sms:
            m=form_mess.cleaned_data.get('messages')
            print(m)
            tel = 375447085046
            mess = f'Клиент {pos.user.username} тел.: {pos.telefon} отправил сообщение: ' + m
            super().sms(request, mess, tel)
            messages.success(request, f'Сообщение отправлено, в ближайшее время вам перезвонят!')
        else:
            mess_deactivation(request, pos.data_input_end_sms)
        return redirect('home')


