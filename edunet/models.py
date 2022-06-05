from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField


# this is the model for users and it inherits AbstractUser
class User(AbstractUser):
    pass


# model for listings
class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    school = models.CharField(max_length=64, default=None, null=True)
    category = models.CharField(max_length=64)
    image_link = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="media", blank=True, default=None)
    classgroup = models.CharField(max_length=64, default=None, null=True)
    starting_bid = models.IntegerField(default=None, null=True)

# model for bids


class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()


# model for comments
class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


# model for watchlist
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()


# model to store the winners
class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)
