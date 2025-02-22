from django import forms
from .models import AuctionListing, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-input'}),
            'description': forms.Textarea(attrs={'class': 'custom-input', 'cols': 80, 'rows': 5}),
            'starting_bid': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.01'}),
            'image_url': forms.URLInput(attrs={'class': 'custom-input'}),
            'category': forms.Select(attrs={'class': 'custom-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False
        self.fields['image_url'].required = False
        
# Forms for bids and comments
class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Your Bid', max_digits=8, decimal_places=2)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))