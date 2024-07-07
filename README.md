**Online Auction Platform**: a ebay-like auction website:



**AuctionHub** is a comprehensive online auction platform built using Django,  providing a complete solution for online auctions, ensuring a smooth user experience and secure transactions. 

####  **Create Listing**
- Users can create a new auction listing by providing a title, description, starting bid, and optionally an image URL and category.
- The listing form is enhanced with custom CSS for a better user experience.

####  **Active Listings Page**
- The default route displays all active auction listings, showing the title, description, current price, and image (if available).
- Listings are presented in a responsive card layout using Bootstrap.

####  **Listing Page**
- Clicking on a listing shows detailed information about the auction, including title, description, current price, category, and the creator's username.
- Users can add/remove the item from their watchlist.
- Users can place bids if they meet the criteria (at least as large as the starting bid and greater than any existing bids).
- The listing creator can close the auction, declaring the highest bidder as the winner.
- Users can add comments, and all comments are displayed on the listing page.
- If a user has won the auction, a congratulatory message is displayed prominently.

####  **Watchlist**
- Users can view their watchlist, which shows all listings they have added.
- Each item in the watchlist is clickable, leading to the detailed listing page.

####  **Categories**
- Users can view all available categories.
- Clicking on a category name displays all active listings in that category.

####  **Django Admin Interface**
- Site administrators can use Django’s admin interface to view, add, edit, and delete any listings, comments, and bids.
- Superuser accounts are created using Django’s `createsuperuser` command.


    ![image](https://github.com/YiTongG/Web-applications/assets/46401538/bdd5ce80-04a8-4682-a963-67475bddb36e)
![image](https://github.com/YiTongG/Web-applications/assets/46401538/06579dd3-7107-48af-9493-dc67f33d8d8c)
![image](https://github.com/YiTongG/Web-applications/assets/46401538/59d6f8ba-1af3-41c7-944a-fd44106d940c)
![image](https://github.com/YiTongG/Web-applications/assets/46401538/2cd546fe-6c5f-4cfa-b263-4972fa9ba7e6)

