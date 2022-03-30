from django import forms
from django.contrib.auth.models import User
from .models import Profile
from ticket.models import Ticket
from django.contrib.auth import authenticate
from rate.models import Rate


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': False,
            'class': 'order__input order__input_email',
        }))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': False
        }))
    remember = forms.BooleanField(
        required=False,
        label='Запомнить меня',
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'check_input'
        }))


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail*')
    password = forms.CharField(label='Пароль*',
                               min_length=8,
                               help_text='Пароль должен содержать как минимум 8 символов',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': False
                               }))
    password2 = forms.CharField(label='Повторите пароль*',
                                min_length=8,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': False
                                }))
    agree = forms.BooleanField(label='Даю согласие на обработку моих персональных данных',
                               initial=True,
                               widget=forms.CheckboxInput(attrs={
                                   'class': 'check_input'
                               }))

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
            raise forms.ValidationError('Пользователь с таким e-mail уже зарегистрирован')
        except User.DoesNotExist:
            return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 8:
            raise forms.ValidationError('Минимальная длина пароля должна быть не меньше 8 символов')
        return cd['password2']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль',
                                   required=False,
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': False,
                                       'autocomplete': 'off',
                                   }))
    password = forms.CharField(label='Пароль',
                               min_length=8,
                               required=False,
                               help_text='Пароль должен содержать как минимум 8 символов',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': False,
                                   'autocomplete': 'off'
                               }))
    password2 = forms.CharField(label='Повторите пароль',
                                min_length=8,
                                required=False,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': False,
                                    'autocomplete': 'off'
                                }))

    def __init__(self, *args, **kwargs):
        """Passing request into form"""
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 8 and len(cd['password2']) > 1:
            raise forms.ValidationError('Минимальная длина пароля должна быть не меньше 8 символов')
        return cd['password2']

    def clean(self):
        user = self.request.user
        cd = self.cleaned_data
        if len(cd['old_password']) > 0:
            check_user = authenticate(self.request,
                                      username=user.email,
                                      password=cd['old_password'])
            if check_user is not None:
                if len(cd['password']) < 8:
                    self.add_error('password', 'Длина нового пароля должна быть не меньше 8 символов')
            else:
                self.add_error('old_password', 'Неправильный пароль')


class ProfileForm(forms.ModelForm):
    fullname = forms.CharField(label='ФИО*',
                               widget=forms.TextInput(attrs={
                                   'placeholder': False
                               }))
    phone = forms.CharField(label='Телефон*',
                            widget=forms.TextInput(attrs={
                                'placeholder': False
                            }))
    city = forms.CharField(label='Город*',
                           widget=forms.TextInput(attrs={
                               'placeholder': False
                           }))
    street = forms.CharField(label='Улица*',
                             widget=forms.TextInput(attrs={
                                 'placeholder': False
                             }))
    house = forms.CharField(label='Дом*',
                            widget=forms.TextInput(attrs={
                                'placeholder': False
                            }))
    apartment = forms.IntegerField(min_value=1, max_value=999999, label='Квартира',
                                   required=False,
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': False
                                   }))

    class Meta:
        model = Profile
        fields = ('fullname', 'phone', 'city', 'street', 'house', 'apartment')


class TicketForm(forms.ModelForm):
    phone = forms.CharField(label='Телефон*',
                            widget=forms.TextInput(attrs={
                                'placeholder': False
                            }))
    city = forms.CharField(label='Город*',
                           widget=forms.TextInput(attrs={
                               'placeholder': False
                           }))
    street = forms.CharField(label='Улица*',
                             widget=forms.TextInput(attrs={
                                 'placeholder': False
                             }))
    house = forms.CharField(label='Дом*',
                            widget=forms.TextInput(attrs={
                                'placeholder': False
                            }))
    apartment = forms.IntegerField(min_value=1, max_value=999999, label='Квартира',
                                   required=False,
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': False
                                   }))
    subject = forms.CharField(label='Тема*',
                              widget=forms.TextInput(attrs={
                                  'placehoder': False
                              }))
    body = forms.CharField(label='Что у вас случилось?*',
                           widget=forms.Textarea(attrs={
                               'placeholder': False,
                               'class': 'order__input order__input_message'
                           }))

    class Meta:
        model = Ticket
        fields = ('phone', 'city', 'street', 'house', 'apartment', 'subject', 'body')


class SubscribeForm(forms.Form):
    rate = forms.ModelChoiceField(queryset=Rate.objects.filter(status='active'),
                                   widget=forms.RadioSelect())

    class Meta:
        fields = ('rate',)
