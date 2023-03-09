from django.db import models
from django.db.models import CheckConstraint, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db.models.constraints import CheckConstraint


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    name = models.CharField(max_length=64)
    status = models.BooleanField(default=1)
    description = models.CharField(max_length=500)
    starting_price = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    current_price = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    image_url = models.URLField(blank=True)

    HOME = 'HO'
    ELECTRONICS = 'EL'
    FASHION = 'FA'
    TOYS = 'TO'
    BOOKS = 'BO'
    OTHER = 'OT'
    CATEGORY_CHOICES = [
        (HOME, 'Home'),
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (OTHER, 'Other')
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    amount = models.PositiveIntegerField(default=1)
    
class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class WatchedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)