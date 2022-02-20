from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Profile
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
            user.username = user.email
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return render(request, 'registration/register_done.html', {'user': user})
        else:
            messages.error(request, 'Исправьте, пожалуйста, ошибки формы')
    else:
        register_form = forms.RegistrationForm()
        profile_form = forms.ProfileForm()
    return render(request, 'registration/register.html',
                  {'register_form': register_form,
                   'profile_form': profile_form})


@login_required
def profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        password_change_form = forms.PasswordChangeForm(data=request.POST, request=request)
        profile_form = forms.ProfileForm(data=request.POST, instance=profile)
        if password_change_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            cd = password_change_form.cleaned_data
            if cd['password']:
                user.set_password(cd['password'])
                user.save()
            if password_change_form.has_changed() or profile_form.has_changed():
                messages.info(request, 'Ваши данные успешно обновлены')
        else:
            messages.error(request, 'Исправьте, пожалуйста, ошибки формы')
    else:
        password_change_form = forms.PasswordChangeForm(request=request)
        profile_form = forms.ProfileForm(instance=profile)
    context = {
        'section': 'profile',
        'password_change_form': password_change_form,
        'profile_form': profile_form,
    }
    return render(request, 'account/profile.html', context)
