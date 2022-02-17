from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request,
                                username=cd['email'],
                                password=cd['password'])
            remember = cd['remember']
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember:
                        request.session.set_expiry(0)
                    return redirect('profile')
                else:
                    messages.warning(request, 'Ваш аккаунт был отключен')
            else:
                messages.error(request, 'Вы ввели неправильный логин или пароль')
    else:
        login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {})
