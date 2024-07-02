from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name='watchlisted_by')


#You will also need to add additional models to this file to represent details about auction listings, bids, comments, and auction categories. 
#Remember that each time you change anything in auctions/models.py, you’ll need to first run python manage.py makemigrations and then python manage.py migrate to migrate those changes to your database.

#auction listings
#bid
#comments
class AuctionListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    current_bid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="wins")

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.bid_amount} by {self.user.username} on {self.listing.title}"
    
class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

