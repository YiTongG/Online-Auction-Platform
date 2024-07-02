from .models import AuctionListing

def watchlist_count(request):
    if request.user.is_authenticated:
        count = request.user.watchlist.count()
    else:
        count = 0
    return {'watchlist_count': count}
