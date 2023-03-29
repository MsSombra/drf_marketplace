from django.db import models
from app_catalog.validators import is_svg
from django.core.exceptions import ValidationError


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("Файл не svg")


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="название")
    parent = models.ForeignKey("self", verbose_name="родитель", on_delete=models.SET_NULL, blank=True,
                               null=True, related_name="subcategories")

    class Meta:
        ordering = "title",
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.title

    def href(self):
        return f"/catalog/{self.pk}"

    def get_absolute_url(self):
        pass


class CategoryImage(models.Model):
    src = models.FileField(upload_to='category_icons/', blank=True, validators=[validate_svg],
                             verbose_name="иконка категории")
    category = models.ForeignKey(Category, related_name="image", verbose_name="категория", on_delete=models.CASCADE)
    alt = models.CharField(max_length=50, verbose_name="описание")

    # @property
    # def src(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url

    class Meta:
        verbose_name = "иконка категории"
        verbose_name_plural = "иконки категорий"


class Specification(models.Model):
    name = models.CharField(max_length=50, db_index=True, blank=False, verbose_name="название")
    value = models.CharField(max_length=50, verbose_name="описание")

    class Meta:
        verbose_name = "характеристика"
        verbose_name_plural = "характеристики"

    def __str__(self):
        return f"{self.name} - {self.value}"


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="название тэга")

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT, verbose_name="категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    count = models.PositiveIntegerField(verbose_name="количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    title = models.CharField(max_length=200, db_index=True, verbose_name="название")
    description = models.TextField(blank=True, null=False, verbose_name="описание")
    fullDescription = models.TextField(blank=True, null=False, verbose_name="полное описание")
    freeDelivery = models.BooleanField(default=False, verbose_name="бесплатная доставка")
    tags = models.ManyToManyField(Tag, related_name="products", verbose_name="тэги")
    specifications = models.ManyToManyField(Specification, related_name="products", verbose_name="характеристика")
    rating = models.FloatField(verbose_name="оценка")

    # reviews = models.PositiveIntegerField(default=0, verbose_name="количество отзывов")
    available = models.BooleanField(default=True, verbose_name="наличие")
    hot_offer = models.BooleanField(default=False, verbose_name="горячее предложение")
    limited_edition = models.BooleanField(default=False, verbose_name="ограниченный тираж")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    @property
    def total_review(self):
        return len(self.reviews.all())

    def href(self):
        return f"/catalog/{self.pk}"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.PROTECT, verbose_name="товар")
    image = models.ImageField(upload_to="products_images/", blank=True, verbose_name="изображение")
    alt = models.CharField(max_length=50, verbose_name="описание")

    @property
    def src(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товаров"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.PROTECT, verbose_name="товар")
    author = models.CharField(max_length=200, db_index=True, verbose_name="автор")
    email = models.EmailField(max_length=50, blank=True, verbose_name="электронная почта")
    text = models.TextField(max_length=200, verbose_name="отзыв")
    rate = models.PositiveIntegerField(verbose_name="оценка")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return self.text

    # def delete(self, *args, **kwargs):
    #     Product.objects.filter(id=self.product.id).update(
    #         reviews=len(Review.objects.filter(product_id=self.product.id) - 1)
    #     )
    #     super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     Product.objects.filter(id=self.product.id).update(
    #         reviews=len(Review.objects.filter(product_id=self.product.id) + 1)
    #     )
    #     super().delete(*args, **kwargs)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sale", verbose_name="товар")
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена со скидкой")
    dateFrom = models.DateTimeField(verbose_name="дата начала действия")
    dateTo = models.DateTimeField(verbose_name="дата окончания действия")

    class Meta:
        verbose_name = "скидка"
        verbose_name_plural = "скидки"
