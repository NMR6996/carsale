from django.urls import path
from . import views

urlpatterns = [
    path("", views.carviews, name=""),
    path("home", views.carviews, name="home"),
    path("index", views.carviews, name="index"),
    path("car_details/<int:id>", views.car_detailed_views, name="car_details"),
    path("cars", views.carviews, name="cars"),
    path("contact", views.contact, name="contact"),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("caradd", views.caradd, name="caradd"),
    path("searchcar", views.searchcar, name="searchcar"),
    path("caredit/<int:id>", views.careditviews, name="caredit"),
    path("favorites/<int:id>/", views.favorites_add, name="favorites_add"),
    path("favorites", views.favorites_list, name="favorites_list"),
    path("elanlar", views.carads_list, name="elanlar"),
    path("elanlar/<int:id>", views.carads_remove, name="carads_remove"),
    path("comment/<int:id>", views.carcomment_add, name="carcomment_add"),
    path("editprofile", views.profile, name="editprofile"),
    path("activate/<uidb64>/<token>", views.activate_user, name="activate"),
    path("reset-password/<uidb64>/<token>", views.reset_password, name="reset-password"),
    path("forget-password", views.forget_password, name="forget-password")
]