from django.conf import settings
from django.db import models, transaction
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


def check_not_parent(category, new_parent):
    if category == new_parent:
        raise ValueError('You try to set category`s chield as it parent')

    else:
        if (elder := new_parent.parent):
            return check_not_parent(category, elder)


@transaction.atomic
def save_product_to_category(product, category):
    category.products.add(product)
    if (parent := category.parent):
        return save_product_to_category(product, parent)


@transaction.atomic
def remove_product_from_category(product, category):
    category.products.remove(product)
    if (parent := category.parent):
        return remove_product_from_category(product, parent)


class RecursiveM2M(models.ManyToManyField):
    @transaction.atomic
    def save_form_data(self, instance, data):
        super().save_form_data(instance, data)
        for category in data.all():
            save_product_to_category(instance, category)


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING,
        null=True, blank=True,
        related_name="chields"
    )

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'
        unique_together = [['name', 'parent']]


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    category = RecursiveM2M(
        ProductCategory, related_name='products',  blank=True
    )

    buskets = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ProductInBusket',
        related_name='busket'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductInBusket(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.owner} - {self.product} - {self.count}'

    def __repr__(self):
        return str(self)

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
        unique_together = [['owner', 'product']]


class ProductImg(models.Model):
    file = models.ImageField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return f'Изображение для {self.product}'

    def __repr__(self):
        return str(self)

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'


@receiver(pre_delete, sender=ProductCategory)
def reset_parent(instance, **kwargs):
    parent = instance.parent
    for category in instance.chields.all():
        category.parent = parent
        category.save(update_fields=['parent'])


@receiver(pre_save, sender=ProductCategory)
@transaction.atomic
def set_product_category(instance, signal, sender, **kwargs):
    if instance.id:
        products = instance.products.all()
        old_parent = ProductCategory.objects.get(id=instance.id).parent
        new_parent = instance.parent

        if new_parent != old_parent:
            if old_parent:
                for product in products:
                    remove_product_from_category(product, old_parent)

            if new_parent:
                check_not_parent(instance, new_parent)

                for product in instance.products.all():
                    save_product_to_category(product, new_parent)
