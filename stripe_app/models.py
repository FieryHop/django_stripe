import stripe
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=50)
    stripe_id = models.CharField(max_length=50, blank=True)
    percent_off = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    name = models.CharField(max_length=50)
    stripe_id = models.CharField(max_length=50, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def create_stripe_tax_rate(self):
        """Создает налоговую ставку в Stripe и возвращает ее ID"""
        stripe.api_key = settings.STRIPE_KEYS['USD']['secret']  # Используем USD по умолчанию
        tax_rate = stripe.TaxRate.create(
            display_name=self.name,
            inclusive=False,
            percentage=float(self.percentage),
            country='US',  # Пример страны
        )
        return tax_rate.id


@receiver(pre_save, sender=Tax)
def create_stripe_tax_rate_handler(sender, instance, **kwargs):
    """Создает налоговую ставку в Stripe перед сохранением Tax"""
    if not instance.stripe_id:
        instance.stripe_id = instance.create_stripe_tax_rate()


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def get_total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id}"


@receiver(pre_save, sender=Discount)
def create_stripe_coupon_handler(sender, instance, **kwargs):
    """Создает купон в Stripe перед сохранением Discount"""
    if not instance.stripe_id:
        instance.stripe_id = instance.create_stripe_coupon()

# Create your models here.
