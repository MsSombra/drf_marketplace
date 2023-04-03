# Generated by Django 4.1.7 on 2023-03-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_express', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена экспресс доставки')),
                ('edge_for_free_delivery', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Порог бесплатной доставки')),
                ('cost_usual_delivery', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена обычной доставки')),
            ],
            options={
                'verbose_name': 'конфигурация',
                'verbose_name_plural': 'конфигурация',
            },
        ),
    ]