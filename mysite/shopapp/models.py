from django.contrib.auth.models import User
from django.db import models


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(null=False, blank=True, verbose_name="описание")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="цена")
    discount = models.SmallIntegerField(default=0, verbose_name="скидка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    archived = models.BooleanField(default=False, verbose_name="архивирован")
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path, verbose_name="превью")

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="продукт")
    image = models.ImageField(upload_to=product_images_directory_path, verbose_name="изображение")
    description = models.CharField(max_length=200, null=False, blank=True, verbose_name="описание")


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    delivery_address = models.TextField(null=True, blank=True, verbose_name="адрес доставки")
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name="промокод")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="пользователь")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="продукты")
    receipt = models.FileField(null=True, upload_to='orders/receipts/', verbose_name="квитанция")