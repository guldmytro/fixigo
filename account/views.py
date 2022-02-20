from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
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
        login_form = forms.LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)
        if register_form.is_valid() and profile_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        register_form = forms.RegistrationForm()
        profile_form = forms.ProfileForm()
    return render(request, 'registration/register.html',
                  {'register_form': register_form,
                   'profile_form': profile_form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {})
