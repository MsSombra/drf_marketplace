from django.core.exceptions import ValidationError
from django.db import models

from app_catalog.validators import is_svg


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("Файл не svg")


class Product(models.Model):
    """ Модель товара """
    category = models.ForeignKey("Category", on_delete=models.SET("undefined"),
                                 related_name="products", verbose_name="категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="цена")
    count = models.IntegerField(default=0, verbose_name="количество")
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="название")
    fullDescription = models.TextField(default="", blank=True, null=False, verbose_name="полное описание")
    freeDelivery = models.BooleanField(default=False, verbose_name="бесплатная доставка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="дата обновления")
    specifications = models.ManyToManyField("Specification", blank=True,
                                            related_name="products", verbose_name="характеристика")
    tags = models.ManyToManyField("Tag", related_name="products", blank=True, verbose_name="тэги")
    limited_edition = models.BooleanField(default=False, verbose_name="ограниченный тираж")
#     hot_offer = models.BooleanField(default=False, verbose_name="горячее предложение")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ("count", )

    def get_absolute_url(self):
        pass

    @property
    def available(self) -> bool:
        """ Наличие товара на складе """
        return self.count > 0

    @property
    def date(self):
        """ Возвращает дату создания """
        return self.created_at

    @property
    def description(self) -> str:
        """ Возвращает краткое описание (первые 100 символов) """
        return self.fullDescription[:100] + "..."

    @property
    def rating(self) -> float:
        """ Возвращает среднее значение рейтинга товара """
        try:
            return round(Review.objects.select_related("product"). \
                         filter(product=self). \
                         aggregate(models.Avg("rate")). \
                         get("rate__avg"), 1)
        except TypeError:
            return 0

    @property
    def href(self) -> str:
        return f"/product/{self.pk}"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """ Модель изображения товара """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="товар")
    image = models.ImageField(upload_to="products_images/", blank=True, verbose_name="изображение")

    class Meta:
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товаров"

    @property
    def src(self) -> str:
        """ Возвращает ссылку на изображение """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def alt(self):
        """ Возвращает наименование товара в качестве описания к изображению """
        return self.product.title

    def __str__(self):
        return self.product.title


class Category(models.Model):
    """ Модель категории товаров """
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="название")
    picture = models.ImageField(upload_to="category_icons/", blank=True, validators=[validate_svg],
                                verbose_name="иконка категории")
    parent = models.ForeignKey("self", verbose_name="родитель", on_delete=models.SET_NULL, blank=True,
                               null=True, related_name="subcategories")

    class Meta:
        ordering = ("title", )
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def image(self) -> dict:
        """ Возвращает ссылку на изображение и описание (насвание категории) """
        return {"src": self.picture.url, "alt": self.title}

    @property
    def href(self) -> str:
        """ Возвращает ссылку на страницу с фильтрацией товаров по категории """
        return f"/catalog/{self.pk}"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass


class Tag(models.Model):
    """ Модель тэга товаров """
    name = models.CharField(max_length=50, unique=True, verbose_name="название тэга")

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return self.name


class RateChoices(models.IntegerChoices):
    """ Enum class for review rate """
    VERY_BAD = 1
    BAD = 2
    NOT_BAD = 3
    GOOD = 4
    VERY_GOOD = 5


class Review(models.Model):
    """ Модель отзыва на товар """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="товар")
    author = models.CharField(max_length=100, blank=True, default="", db_index=True, verbose_name="автор")
    email = models.EmailField(blank=True, default="", verbose_name="электронная почта")
    text = models.TextField(blank=True, default="", verbose_name="отзыв")
    rate = models.PositiveIntegerField(choices=RateChoices.choices, default=RateChoices.VERY_GOOD,
                                       verbose_name="оценка")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f'{self.author} - {self.product.title}'


class Specification(models.Model):
    """ Модель характеристик товара """
    name = models.CharField(max_length=50, db_index=True, blank=False, verbose_name="название")
    value = models.CharField(max_length=50, verbose_name="описание")

    class Meta:
        verbose_name = "характеристика"
        verbose_name_plural = "характеристики"
        unique_together = ("name", "value")

    def __str__(self):
        return f"{self.name} - {self.value}"


class Sale(models.Model):
    """ Модель скидки на товар """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sale", verbose_name="товар")
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="цена со скидкой")
    dateFrom = models.DateTimeField(verbose_name="дата начала действия")
    dateTo = models.DateTimeField(verbose_name="дата окончания действия")

    class Meta:
        verbose_name = "скидка"
        verbose_name_plural = "скидки"

    def __str__(self):
        return f"{self.product.title}: {self.dateFrom} - {self.dateTo}"
