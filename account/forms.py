from django import forms
from django.contrib.auth.models import User
from .models import Profile


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
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Пароль*',
                               min_length=8,
                               help_text='Пароль должен содержать как минимум 8 символов',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': False
                               }))
    password2 = forms.CharField(label='Повторите пароль*',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': False
                                }))

    class Meta:
        model = User
        fields = ('username', 'email')

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
                                   widget=forms.NumberInput(attrs={
                                       'placeholder': False
                                   }))

    class Meta:
        model = Profile
        fields = ('fullname', 'phone', 'city', 'street', 'house', 'apartment')
