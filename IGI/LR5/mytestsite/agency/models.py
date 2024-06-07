from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Climate(models.Model):
    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    ]
    season = models.CharField(max_length=100, choices=SEASON_CHOICES)
    description = models.TextField()
    avg_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    avg_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    avg_pressure = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return (
            f"{self.season}: {self.description}, "
            f"Temp: {self.avg_temperature}°C, "
            f"Humidity: {self.avg_humidity}%, "
            f"Pressure: {self.avg_pressure} hPa")


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    standard_room_price = models.DecimalField(max_digits=8, decimal_places=2)
    vip_room_price = models.DecimalField(max_digits=8, decimal_places=2)
    country = models.ForeignKey('Country', related_name='hotels', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)
    climate_winter = models.OneToOneField(Climate, related_name='winter_country', on_delete=models.CASCADE, null=True,
                                          blank=True)
    climate_spring = models.OneToOneField(Climate, related_name='spring_country', on_delete=models.CASCADE, null=True,
                                          blank=True)
    climate_summer = models.OneToOneField(Climate, related_name='summer_country', on_delete=models.CASCADE, null=True,
                                          blank=True)
    climate_autumn = models.OneToOneField(Climate, related_name='autumn_country', on_delete=models.CASCADE, null=True,
                                          blank=True)

    def __str__(self):
        return self.name


class TravelPackage(models.Model):
    name = models.CharField(max_length=50, default="Default Travel Package")
    DURATION_CHOICES = [
        (7, '1 week'),
        (14, '2 weeks'),
        (28, '4 weeks')
    ]
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    duration_days = models.IntegerField(choices=DURATION_CHOICES)
    intermediate_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.name}:{self.hotel}, {self.duration_days}d."
        )


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%| Active:{self.active}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    birth_date = models.DateField()
    belarus_phone_number = models.CharField(max_length=13, validators=[
        RegexValidator(regex=r'^\+375\d{9}$', message="Valid format +375XXXXXXXXX")])
    promo_codes = models.ManyToManyField(PromoCode, blank=True)

    def total_orders(self):
        return self.orders.count()

    def total_spent(self):
        return sum(order.final_price for order in self.orders.all())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stuff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Order(models.Model):
    STATUS_CHOICES = [
        ('PR', 'In processing'),
        ('AC', 'Active'),
        ('IN', 'Inactive')
    ]
    package = models.ForeignKey('TravelPackage', on_delete=models.SET_NULL, null=True)
    promo_code_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    departure_date = models.DateField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='orders')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.package:
            self.final_price = self.package.intermediate_price
            if self.promo_code:
                self.promo_code_discount = self.promo_code.discount_percentage
                self.final_price -= (self.final_price * self.promo_code_discount) / 100
            hotel_price = self.package.hotel.standard_room_price
            self.final_price += hotel_price * self.package.duration_days
            print(f"{self.package.duration_days} - {self.amount}")
            self.final_price *= int(self.amount)

        super().save(*args, **kwargs)


@receiver(pre_save, sender=PromoCode)
def update_active_field(sender, instance, **kwargs):
    if instance.valid_to < timezone.now():
        instance.active = False
