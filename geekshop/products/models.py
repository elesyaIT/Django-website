from django.db import models


# Create your models here.

class ProductsCategory(models.Model):
    name = models.CharField(verbose_name='Название категории',max_length=64)
    description = models.TextField(verbose_name='Описание категории',blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название продукта',max_length=64)
    image = models.ImageField(verbose_name='Фото продукта',upload_to='products_images',blank=True)
    description = models.TextField(verbose_name='Описание продукта',blank=True,null=True)
    price = models.DecimalField(verbose_name='Цена продукта',max_digits=8,decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Кол-во продукта',default=0)
    category = models.ForeignKey(ProductsCategory,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return  f'{self.name} | {self.category}'

