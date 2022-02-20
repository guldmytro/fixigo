from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fullname = models.CharField(max_length=200, verbose_name='ФИО', blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=200, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=10, verbose_name='Дом', blank=True, null=True)
    apartment = models.PositiveSmallIntegerField(verbose_name='Квартира', blank=True, null=True)

    def __str__(self):
        return f'Профиль {self.fullname}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
