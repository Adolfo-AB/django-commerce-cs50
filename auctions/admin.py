from django.contrib import admin
from .models import Listing, Bid, Comment, WatchedListing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status" )

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user", "listing")

class WatchedListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")
		
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchedListing)
