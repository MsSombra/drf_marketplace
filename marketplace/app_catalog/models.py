from app_account.models import Profile
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="название")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="ссылка")
    chosen = models.BooleanField(default=False, verbose_name="избранная категория")
    icon = models.ImageField(upload_to="categories_icons/", blank=True, verbose_name="иконка")

    class Meta:
        ordering = "name",
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass


class Specification(models.Model):
    name = models.CharField(max_length=50, db_index=True, blank=False, verbose_name="название")
    value = models.CharField(max_length=50, verbose_name="описание")

    class Meta:
        verbose_name = "характеристика"
        verbose_name_plural = "характеристики"

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT, verbose_name="категория")
    specifications = models.ManyToManyField(Specification, related_name="products", verbose_name="характеристика")
    title = models.CharField(max_length=200, db_index=True, verbose_name="название")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="ссылка")
    description = models.TextField(blank=True, null=False, verbose_name="описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    available = models.BooleanField(default=True, verbose_name="наличие")
    count = models.PositiveIntegerField(verbose_name="количество")
    hot_offer = models.BooleanField(default=False, verbose_name="горячее предложение")
    limited_edition = models.BooleanField(default=False, verbose_name="ограниченный тираж")
    reviews = models.PositiveIntegerField(default=0, verbose_name="количество отзывов")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        index_together = (("id", "slug"),)

    def get_absolute_url(self):
        pass


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.PROTECT, verbose_name="товар")
    img = models.ImageField(upload_to="products_img/", blank=True, verbose_name="изображение")


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="review", on_delete=models.PROTECT, verbose_name="товар")
    author = models.CharField(max_length=200, db_index=True, verbose_name="автор")
    email = models.EmailField(max_length=50, blank=True, verbose_name="электронная почта")
    text = models.TextField(max_length=200, verbose_name="отзыв")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return self.text

    def delete(self, *args, **kwargs):
        Product.objects.filter(id=self.product.id).update(
            reviews=len(Review.objects.filter(product_id=self.product.id) - 1)
        )
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        Product.objects.filter(id=self.product.id).update(
            reviews=len(Review.objects.filter(product_id=self.product.id) + 1)
        )
        super().delete(*args, **kwargs)
