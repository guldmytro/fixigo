from django.db import models
from account.models import Profile
from django.utils import timezone
from django.urls import reverse


class UnreadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='unread')


class ReadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='read')


class Notification(models.Model):
    STATUS_CHOICES = (
        ('unread', 'Непрочитанные'),
        ('read', 'Прочитанные')
    )
    profile = models.ForeignKey(Profile, related_name='notifications', verbose_name='Профиль', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст')
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, default='unread', max_length=6)
    publish = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    unread = UnreadManager()
    read = ReadManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification_detail', kwargs={'notification_id': self.pk})
