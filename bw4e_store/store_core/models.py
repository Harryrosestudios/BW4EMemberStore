from django.db import models
from django.contrib.auth.models import User

class Partner(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('discount', 'Discount'),
        ('promotion', 'Promotion'),
        ('service', 'Service'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) # Assuming an 'product_images/' upload path
    terms_and_conditions = models.TextField(blank=True, null=True)
    redeemable_once = models.BooleanField(default=False)
    available_from = models.DateTimeField(blank=True, null=True)
    available_to = models.DateTimeField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} by {self.partner.name}"

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    partner_confirmation_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Confirmation ID from partner system, if applicable"
    )

    def __str__(self):
        return f"{self.user.username} redeemed {self.product.name}"
