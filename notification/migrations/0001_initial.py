# Generated by Django 4.0.2 on 2022-02-21 08:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Текст')),
                ('status', models.CharField(choices=[('unread', 'Непрочитанные'), ('read', 'Прочитанные')], default='unread', max_length=6, verbose_name='Статус')),
                ('publish', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='account.profile', verbose_name='Профиль')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]