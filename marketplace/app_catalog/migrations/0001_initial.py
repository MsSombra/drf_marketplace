# Generated by Django 4.1.7 on 2023-07-05 13:51

import app_catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='название')),
                ('picture', models.FileField(blank=True, upload_to='category_icons/', validators=[app_catalog.models.validate_svg], verbose_name='иконка категории')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='app_catalog.category', verbose_name='родитель')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='цена')),
                ('count', models.IntegerField(default=0, verbose_name='количество')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='название')),
                ('fullDescription', models.TextField(blank=True, default='', verbose_name='полное описание')),
                ('freeDelivery', models.BooleanField(default=False, verbose_name='бесплатная доставка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
                ('limited_edition', models.BooleanField(default=False, verbose_name='ограниченный тираж')),
                ('category', models.ForeignKey(on_delete=models.SET('undefined'), related_name='products', to='app_catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('count',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название тэга')),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='название')),
                ('value', models.CharField(max_length=50, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'характеристика',
                'verbose_name_plural': 'характеристики',
                'unique_together': {('name', 'value')},
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='цена со скидкой')),
                ('dateFrom', models.DateTimeField(verbose_name='дата начала действия')),
                ('dateTo', models.DateTimeField(verbose_name='дата окончания действия')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='app_catalog.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'скидка',
                'verbose_name_plural': 'скидки',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, db_index=True, default='', max_length=100, verbose_name='автор')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='электронная почта')),
                ('text', models.TextField(blank=True, default='', verbose_name='отзыв')),
                ('rate', models.PositiveIntegerField(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Not Bad'), (4, 'Good'), (5, 'Very Good')], default=5, verbose_name='оценка')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_catalog.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='products_images/', verbose_name='изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_catalog.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'изображение товара',
                'verbose_name_plural': 'изображения товаров',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(blank=True, related_name='products', to='app_catalog.specification', verbose_name='характеристика'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='app_catalog.tag', verbose_name='тэги'),
        ),
    ]
