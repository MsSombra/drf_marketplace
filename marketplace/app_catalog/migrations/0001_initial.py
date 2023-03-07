# Generated by Django 4.1.7 on 2023-03-07 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='название')),
                ('slug', models.SlugField(max_length=200, verbose_name='ссылка')),
                ('chosen', models.BooleanField(default=False, verbose_name='избранная категория')),
                ('icon', models.ImageField(blank=True, upload_to='categories_icons/', verbose_name='иконка')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='название')),
                ('slug', models.SlugField(max_length=200, verbose_name='ссылка')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('available', models.BooleanField(default=True, verbose_name='наличие')),
                ('amount', models.PositiveIntegerField(verbose_name='количество')),
                ('hot_offer', models.BooleanField(default=False, verbose_name='горячее предложение')),
                ('limited_edition', models.BooleanField(default=False, verbose_name='ограниченный тираж')),
                ('reviews', models.PositiveIntegerField(default=0, verbose_name='количество отзывов')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='app_catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='название')),
                ('description', models.CharField(max_length=50, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'характеристика',
                'verbose_name_plural': 'характеристики',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_account.profile', verbose_name='автор')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review', to='app_catalog.product', verbose_name='товар')),
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
                ('img', models.ImageField(blank=True, upload_to='products_img/', verbose_name='изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='image', to='app_catalog.product', verbose_name='товар')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(related_name='products', to='app_catalog.specification', verbose_name='характеристика'),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'slug')},
        ),
    ]