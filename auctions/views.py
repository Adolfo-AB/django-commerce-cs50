from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, WatchedListing
from .forms import ListingForm

def index(request):
    listings = Listing.objects.filter(status=1)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def closed_listings(request):
    listings = Listing.objects.filter(status=0)
    return render(request, "auctions/closed_listings.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    category = next((item for item in Listing.CATEGORY_CHOICES if item[0] == listing.category), None)
    comments = Comment.objects.filter(user=request.user, listing=listing)
    
    highest_bidder = Utils.find_highest_bidder(listing)

    if request.user.is_authenticated:
        watchlist_label = Utils.find_watchlist_label(listing, request.user)
        if request.user == listing.seller:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": category,
                "seller": True,
                "comments": comments,
                "highest_bidder": highest_bidder})
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": category,
                "watchlist_label": watchlist_label,
                "comments": comments,
                "highest_bidder": highest_bidder})
    else:
        return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": category,
                "comments": comments,
                "highest_bidder": highest_bidder})

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    category = next((item for item in Listing.CATEGORY_CHOICES if item[0] == listing.category), None)
    comments = Comment.objects.filter(user=request.user, listing=listing)
    highest_bidder = Utils.find_highest_bidder(listing)
    
    if request.method == "POST":
        try:
            new_bid = int(request.POST["current_price"])
        except:
           return render(request, "auctions/listing.html", {
                                    "listing": listing,
                                    "category": category,
                                    "comments": comments,
                                    "highest_bidder": highest_bidder}) 

        watchlist_label = Utils.find_watchlist_label(listing, request.user)
        if new_bid > listing.current_price:
            listing.current_price = new_bid
            listing.save()
            bid = Bid(listing=listing, user=request.user, amount=new_bid)
            bid.save()
            return render(request, "auctions/listing.html", {
                                    "listing": listing,
                                    "category": category,
                                    "watchlist_label": watchlist_label,
                                    "message": "You have successfully bid on this product",
                                    "comments": comments,
                                    "highest_bidder": highest_bidder})
        else:
            return render(request, "auctions/listing.html", {
                                    "listing": listing,
                                    "category": category,
                                    "watchlist_label": watchlist_label,
                                    "message": "The bid should be higher than the current price.",
                                    "comments": comments,
                                    "highest_bidder": highest_bidder})

@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    category = next((item for item in Listing.CATEGORY_CHOICES if item[0] == listing.category), None)
    comments = Comment.objects.filter(user=request.user, listing=listing)
    highest_bidder = Utils.find_highest_bidder(listing)

    if request.method == "POST":
        comment = Comment(user=request.user, text=request.POST["comment"], listing=listing)
        comment.save()
        if request.user == listing.seller:
            return render(request, "auctions/listing.html", {
                                        "listing": listing,
                                        "category": category,
                                        "watchlist_label": Utils.find_watchlist_label(listing, request.user),
                                        "seller": True,
                                        "comments": comments,
                                        "highest_bidder": highest_bidder})
        else:
            return render(request, "auctions/listing.html", {
                                        "listing": listing,
                                        "category": category,
                                        "watchlist_label": Utils.find_watchlist_label(listing, request.user),
                                        "comments": comments,
                                        "highest_bidder": highest_bidder})

@login_required
def new_listing(request):
    return render(request, 'auctions/new_listing.html', {
        "form": ListingForm()
    })

@login_required
def add(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        listing = Listing(seller=request.user, name=name, status=1, description=description, image_url=image_url, category=category, starting_price=1, current_price=1)

        try:
            starting_price = int(request.POST["starting_price"])

            if starting_price >= 1:
                listing.starting_price = starting_price
                listing.current_price = starting_price
                listing.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                form = ListingForm(name=name, description=description, image_url=image_url, category=category)
                return render(request, 'auctions/new_listing.html', {
                                "form": form
                            })
        except:
           pass

@login_required
def watch_unwatch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    category = next((item for item in Listing.CATEGORY_CHOICES if item[0] == listing.category), None)
    comments = Comment.objects.filter(user=request.user, listing=listing)
    highest_bidder = Utils.find_highest_bidder(listing)
    
    if WatchedListing.objects.filter(user=request.user, listing=listing).exists():
        watched_listing = WatchedListing.objects.get(user=request.user, listing=listing)
        watched_listing.delete()

        return render(request, "auctions/listing.html", {
                                    "listing": listing,
                                    "category": category,
                                    "unwatched": True,
                                    "watchlist_label": "Add to watchlist",
                                    "comments": comments,
                                    "highest_bidder": highest_bidder})
    
    else:
        watched_listing = WatchedListing(user=request.user, listing=listing)
        watched_listing.save()
        return render(request, "auctions/listing.html", {
                                    "listing": listing,
                                    "category": category,
                                    "watched": True,
                                    "watchlist_label": "Remove from watchlist",
                                    "comments": comments,
                                    "highest_bidder": highest_bidder})

@login_required
def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        category = next((item for item in Listing.CATEGORY_CHOICES if item[0] == listing.category), None)
        comments = Comment.objects.filter(user=request.user, listing=listing)
        highest_bidder = Utils.find_highest_bidder(listing)

        listing.status = 0
        listing.save()

        return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": category,
                "seller": True,
                "closed": True,
                "comments": comments,
                "highest_bidder": highest_bidder})

@login_required
def watchlist(request):
    listings = []
    if WatchedListing.objects.filter(user=request.user).exists():
        watchlist = WatchedListing.objects.filter(user=request.user)
        for item in watchlist:
            listings.append(item.listing)

    return render(request, "auctions/watchlist.html", {
        "listings": listings})

def categories(request):
    categories = [category[1] for category in Listing.CATEGORY_CHOICES]
    return render(request, "auctions/categories.html", {
                            "categories": categories})

def category_listings(request, category):
    category = next((item for item in Listing.CATEGORY_CHOICES if item[1] == category), None)
    listings = Listing.objects.filter(category=category[0], status=1).all()
    return render(request, "auctions/category_listings.html", {
                            "category": category,
                            "listings": listings})

class Utils():
    def find_watchlist_label(listing, user):
        if WatchedListing.objects.filter(user=user, listing=listing).exists():
            return "Remove from watchlist"
        else:
            return "Add to watchlist"

    def find_highest_bidder(listing):
        try:
            highest_bidder = Bid.objects.filter(listing=listing).last().user
            return highest_bidder
        except:
            pass

