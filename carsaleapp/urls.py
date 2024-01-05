from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("otp/<str:username>/<str:phone_number>", views.on_time_password, name="otp"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("forget_password", views.forget_password_request, name="forget-password"),
    path("reset_password/<str:username>", views.reset_password_request, name="reset-password"),

    path("", views.carviews, name=""),
    path("home", views.carviews, name="home"),
    path("index", views.carviews, name="index"),

    path("cars", views.carviews, name="cars"),
    path("caradd", views.caradd, name="caradd"),
    path("car_details/<int:id>", views.car_detailed_views, name="car_details"),
    path("caredit/<int:id>", views.careditviews, name="caredit"),

    path("favorites", views.favorites_list, name="favorites_list"),
    path("favorites/<int:id>/", views.favorites_add, name="favorites_add"),

    path("elanlar", views.carads_list, name="elanlar"),
    path("elanlar/<int:id>", views.carads_remove, name="carads_remove"),

    path("searchcar", views.searchcar, name="searchcar"),
    path("comment/<int:id>", views.carcomment_add, name="carcomment_add"),
    path("contact", views.contact, name="contact"),
    path("editprofile", views.profile, name="editprofile"),

]
