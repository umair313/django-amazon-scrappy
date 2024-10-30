from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    asin = models.CharField(max_length=50, unique=True)
    image_url = models.URLField(max_length=200)
    product_url = models.URLField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title
