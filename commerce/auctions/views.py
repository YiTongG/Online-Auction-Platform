from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse

from .models import User
from .models import AuctionListing,Bid, Comment,User,Category
from .forms import ListingForm,BidForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max

def index(request):
    active_listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "active_listings": active_listings
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

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()
            return redirect('index')  # Redirect to the active listings page
    else:
        form = ListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})


def listing_page(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    is_owner = request.user == listing.creator
    has_won = False
    if listing.winner:
        has_won = request.user == listing.winner

    bid_form = BidForm()
    comment_form = CommentForm()
    error_message = None

    if request.method == 'POST':
        if 'place_bid' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_amount = bid_form.cleaned_data['bid_amount']
                current_max_bid = listing.bids.order_by('-bid_amount').first()
                if current_max_bid:
                    current_max_bid = current_max_bid.bid_amount
                else:
                    current_max_bid = listing.starting_bid
                if bid_amount > current_max_bid:
                    new_bid = Bid(listing=listing, user=request.user, bid_amount=bid_amount)
                    new_bid.save()
                    listing.current_bid = bid_amount
                    listing.save()
                else:
                    error_message = 'Bid must be higher than the current bid.'
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = Comment(listing=listing, user=request.user, content=comment_form.cleaned_data['content'])
                new_comment.save()
        elif 'add_to_watchlist' in request.POST:
            request.user.watchlist.add(listing)
        elif 'remove_from_watchlist' in request.POST:
            request.user.watchlist.remove(listing)

    return render(request, 'auctions/listing_page.html', {
        'listing': listing,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': listing.comments.all(),
        'is_owner': is_owner,
        'has_won': has_won,
        'error_message': error_message,
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user != listing.creator:
        return HttpResponseForbidden("You are not allowed to close this auction.")
    listing.active = False
    highest_bid = listing.bids.order_by('-bid_amount').first()
    if highest_bid:
        listing.winner = highest_bid.user
    listing.save()
    return redirect('listing_page', listing_id=listing_id)

def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = AuctionListing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    request.user.watchlist.add(listing)
    return redirect('listing_page', listing_id=listing_id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    request.user.watchlist.remove(listing)
    return redirect('watchlist')