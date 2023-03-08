# Generated by Django 4.1.7 on 2023-03-08 16:55

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_account', '0001_initial'),
        ('app_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(db_index=True, max_length=100, verbose_name='ФИО')),
                ('email', models.EmailField(blank=True, max_length=50, verbose_name='электронная почта')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('payment_type', models.CharField(max_length=15, verbose_name='тип оплаты')),
                ('delivery_type', models.CharField(max_length=15, verbose_name='тип доставки')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма заказа')),
                ('city', models.CharField(max_length=40, verbose_name='город')),
                ('address', models.CharField(max_length=40, verbose_name='адрес')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app_account.profile', verbose_name='покупатель')),
                ('products', models.ManyToManyField(related_name='orders', to='app_catalog.product', verbose_name='товары')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='название')),
            ],
            options={
                'verbose_name': 'статус заказа',
                'verbose_name_plural': 'статусы заказа',
            },
        ),
        migrations.CreateModel(
            name='ProductsInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='количество товара в заказе')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_catalog.product', verbose_name='товар')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='app_orders.orderstatus', verbose_name='статус заказа'),
        ),
    ]
