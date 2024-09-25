from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    current_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.CharField(max_length=500)
    time = models.TimeField()

class Category(models.Model):
    cat_title = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.cat_title}"

class Image(models.Model):
    image = models.ImageField()

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listed")
    title = models.CharField(max_length=64)
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bids")
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="comments")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.title} {self.bid}, {self.category}"