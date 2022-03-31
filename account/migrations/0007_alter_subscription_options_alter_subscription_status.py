# Generated by Django 4.0.2 on 2022-03-31 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_subscription_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ('-created', '-begin'), 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('active', 'Активный'), ('archive', 'Архивный'), ('waiting_for_pay', 'В ожидании оплаты'), ('pending', 'В процессе активации')], max_length=20, verbose_name='Статус'),
        ),
    ]
