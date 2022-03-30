from django.db import models
from django.contrib.auth import get_user_model
import datetime

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


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активный'),
        ('archive', 'Архивный'),
        ('pending', 'В процессе активации')
    )
    TIME_CHOICES = (
        ('month', 'Месяц'),
        ('year', 'Год')
    )
    title = models.CharField(max_length=150, verbose_name='Название')
    timedelta = models.CharField(max_length=10, verbose_name='Продолжительность', choices=TIME_CHOICES)
    profile = models.ForeignKey(Profile, related_name='subscribtions', verbose_name='Профиль', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    paid = models.BooleanField(default=False, verbose_name='Оплачено?')
    begin = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES)

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def days_left(self):
        if self.end:
            days_left = (datetime.date(year=self.end.year, month=self.end.month, day=self.end.day)
                         - datetime.date.today()).days
            if days_left > 0:
                return days_left
        return False

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-begin',)
