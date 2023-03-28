# Generated by Django 4.1.7 on 2023-03-28 16:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


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
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('fullName', models.CharField(db_index=True, max_length=100, verbose_name='ФИО')),
                ('email', models.EmailField(blank=True, max_length=50, verbose_name='электронная почта')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='номер телефона')),
                ('deliveryType', models.CharField(max_length=30, verbose_name='тип доставки')),
                ('paymentType', models.CharField(max_length=30, verbose_name='тип оплаты')),
                ('delivery_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена доставки')),
                ('status', models.CharField(blank=True, max_length=150, null=True, verbose_name='статус платежа')),
                ('city', models.CharField(max_length=40, verbose_name='город')),
                ('address', models.CharField(max_length=40, verbose_name='адрес')),
                ('card_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)], verbose_name='Номер карты')),
                ('payment_code', models.IntegerField(default=0, verbose_name='Код оплаты')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app_account.profile', verbose_name='покупатель')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='ProductsInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_orders.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='app_catalog.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'товары',
                'verbose_name_plural': 'товары',
            },
        ),
    ]
