from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    on_sale = models.BooleanField(default=False)

    @property
    def tax(self):
        return self.price * 0.3