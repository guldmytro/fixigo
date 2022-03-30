# Generated by Django 4.0.2 on 2022-03-21 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('timedelta', models.CharField(choices=[('month', 'Месяц'), ('year', 'Год')], max_length=10, verbose_name='Продолжительность')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачено?')),
                ('begin', models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('archive', 'Архивный'), ('pending', 'В процессе активации')], max_length=10, verbose_name='Статус')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribtions', to='account.profile', verbose_name='Профиль')),
            ],
        ),
    ]
