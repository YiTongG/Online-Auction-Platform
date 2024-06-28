from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse

from .models import User
from .models import AuctionListing,Bid, Comment
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
    has_won = listing.winner == request.user if listing.winner else False

    if request.method == 'POST':
        if 'place_bid' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_amount = bid_form.cleaned_data['bid_amount']
                current_max_bid = listing.bids.aggregate(Max('bid_amount'))['bid_amount__max'] or listing.starting_bid
                if bid_amount > current_max_bid:
                    Bid.objects.create(listing=listing, user=request.user, bid_amount=bid_amount)
                    listing.current_bid = bid_amount
                    listing.save()
                else:
                    return render(request, 'auctions/listing_page.html', {'listing': listing, 'error': 'Your bid must be higher than the current bid.', 'bid_form': bid_form, 'comment_form': CommentForm()})
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                Comment.objects.create(listing=listing, user=request.user, content=comment_form.cleaned_data['content'])

    else:
        bid_form = BidForm()
        comment_form = CommentForm()

    comments = Comment.objects.filter(listing=listing)
    return render(request, 'auctions/listing_page.html', {
        'listing': listing,
        'is_owner': is_owner,
        'has_won': has_won,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': comments
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Ensure that only the creator can close the auction
    if request.user != listing.creator:
        return HttpResponseForbidden("You are not allowed to close this auction.")
    
    if request.method == 'POST':
        listing.active = False
        highest_bid = listing.bids.order_by('-bid_amount').first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.save()
        return redirect('listing_page', listing_id=listing_id)
    
    return render(request, 'auctions/close_auction.html', {'listing': listing})