from django import forms


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
