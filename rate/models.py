from django.db import models


class Rate(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активный'),
        ('archive', 'Архивный')
    )
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price_year = models.PositiveIntegerField(verbose_name='Цена за год', blank=True, null=True)
    price_month = models.PositiveIntegerField(verbose_name='Цена за месяц', blank=True, null=True)
    status = models.CharField(max_length=8, verbose_name='Статус', choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('price_year', 'price_month')
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'
