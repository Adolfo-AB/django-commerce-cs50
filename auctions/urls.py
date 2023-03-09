from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("new_listing/add", views.add, name="add"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid"),
    path("listings/<int:listing_id>/comment", views.comment, name="comment"),
    path("listings/<int:listing_id>/close", views.close, name="close"),
    path("listings/<int:listing_id>/watch", views.watch_unwatch, name="watch_unwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
