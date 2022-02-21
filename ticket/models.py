from django.db import models
from account.models import Profile
from django.urls import reverse


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Новая заявка', 'Новая заявка'),
        ('На рассмотрении', 'На рассмотрении'),
        ('В работе', 'В работе'),
        ('Завершено', 'Завершено')
    )
    profile = models.ForeignKey(Profile, related_name='tickets', verbose_name='Профиль', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, verbose_name='Тема')
    status = models.CharField(max_length=50, verbose_name='Статус', choices=STATUS_CHOICES, default='Новая заявка')
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=200, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=10, verbose_name='Дом', blank=True, null=True)
    apartment = models.PositiveSmallIntegerField(verbose_name='Квартира', blank=True, null=True)
    body = models.TextField(max_length=500, verbose_name='Что случилось')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Оновлено')

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'ticket_id': self.pk})
