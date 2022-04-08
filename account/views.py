from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Profile
from notification.models import Notification
from ticket.models import Ticket
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import Subscription
import requests
from .utils import register_order


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
                re_user = authenticate(request,
                                       username=user.email,
                                       password=cd['password'])
                login(request, re_user)

            if password_change_form.has_changed() or profile_form.has_changed():
                messages.info(request, 'Ваши данные успешно обновлены')
        else:
            messages.error(request, 'Исправьте, пожалуйста, ошибки формы')
    else:
        password_change_form = forms.PasswordChangeForm(request=request)
        profile_form = forms.ProfileForm(instance=profile)

    breadcrumbs = [
        {
            'link': False,
            'label': 'Профиль'
        }
    ]
    context = {
        'section': 'profile',
        'password_change_form': password_change_form,
        'profile_form': profile_form,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/profile.html', context)


@login_required
def notifications_list(request, unread=None):
    profile_obj = request.user.profile
    if unread == 'unread':
        notifications_object = Notification.unread.filter(profile=profile_obj)
    else:
        notifications_object = Notification.objects.filter(profile=profile_obj)
    paginator = Paginator(notifications_object, 10)
    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    breadcrumbs = [
        {
            'link': False,
            'label': 'Уведомления'
        }
    ]
    context = {
        'notifications': notifications,
        'section': 'notifications',
        'unread': unread,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/notifications.html', context)


@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, profile=request.user.profile)
    if notification.status == 'unread':
        notification.status = 'read'
        notification.save()

    breadcrumbs = [
        {
            'link': reverse('notifications'),
            'label': 'Уведомления'
        },
        {
            'link': False,
            'label': notification.title
        }
    ]
    context = {
        'notification': notification,
        'section': 'notifications',
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'account/notification_detail.html', context)


@login_required
def tickets_list(request):
    profile_obj = request.user.profile
    tickets_object = Ticket.objects.filter(profile=profile_obj).order_by('-created')
    paginator = Paginator(tickets_object, 10)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    breadcrumbs = [
        {
            'link': False,
            'label': 'Мои заявки'
        }
    ]
    context = {
        'section': 'tickets',
        'tickets': tickets,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/tickets.html', context)


@login_required
def ticket_detail(request, ticket_id):
    profile_obj = request.user.profile
    ticket = get_object_or_404(Ticket, pk=ticket_id, profile=profile_obj)

    breadcrumbs = [
        {
            'link': reverse('tickets_list'),
            'label': 'Мои заявки'
        },
        {
            'link': False,
            'label': ticket.subject
        }
    ]
    context = {
        'section': 'tickets',
        'ticket': ticket,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/ticket_detail.html', context)


@login_required
def tickets_add(request):
    profile_obj = request.user.profile
    if request.method == 'POST':
        ticket_form = forms.TicketForm(data=request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.profile = profile_obj
            ticket.save()
            messages.info(request, 'Ваша заявка успешно создана')
            return redirect('tickets_list')
        else:
            messages.error(request, 'Исправьте, пожалуйста, ошибки формы')
    else:
        ticket_form = forms.TicketForm(initial={
            'phone': profile_obj.phone,
            'city': profile_obj.city,
            'street': profile_obj.street,
            'house': profile_obj.house,
            'apartment': profile_obj.apartment
        })
    breadcrumbs = [
        {
            'link': reverse('tickets_list'),
            'label': 'Мои заявки'
        },
        {
            'link': False,
            'label': 'Новая заявка'
        }
    ]
    context = {
        'section': 'tickets',
        'ticket_form': ticket_form,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/ticket_add.html', context)


@login_required
def subscribe_list(request):
    breadcrumbs = [
        {
            'link': False,
            'label': 'Мои подписки'
        }
    ]
    profile = Profile.objects.get(user=request.user)
    subscriptions_obj = Subscription.objects.filter(paid=True, profile=profile)
    paginator = Paginator(subscriptions_obj, 10)
    page = request.GET.get('page')
    try:
        subscriptions = paginator.page(page)
    except PageNotAnInteger:
        subscriptions = paginator.page(1)
    except EmptyPage:
        subscriptions = paginator.page(paginator.num_pages)

    context = {
        'subscriptions': subscriptions,
        'section': 'subscribe',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'account/subscribe.html', context)


@login_required
def subscribe_add(request):

    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            cd = subscribe_form.cleaned_data
            subscribtion = Subscription()
            rate = cd['rate']
            subscribtion.title = rate.title
            subscribtion.timedelta = cd['period']
            if cd['period'] == 'month':
                subscribtion.price = rate.price_month
            else:
                subscribtion.price = rate.price_year
            subscribtion.profile = request.user.profile
            subscribtion.paid = False
            subscribtion.status = 'waiting_for_pay'
            subscribtion.save()
            # register_order(subscribtion.price)
            # ...
        else:
            messages.error(request, 'Выберите тарифный план и срок из списка')
    else:
        subscribe_form = forms.SubscribeForm()
    breadcrumbs = [
        {
            'link': reverse('subscribe_list'),
            'label': 'Мои подписки'
        },
        {
            'link': False,
            'label': 'Оформить / изменить подписку'
        }
    ]
    context = {
        'subscribe_form': subscribe_form,
        'breadcrumbs': breadcrumbs,
        'section': 'subscribe',
    }
    return render(request, 'account/subscribe_add.html', context)
