from django.contrib import admin
from .models import Caradd, Comment, Contact, CaraddInfo, CarMultipleImages, Profile


# Register your models here.
class Admincar(admin.ModelAdmin):
    list_display = ['user', 'brand', 'model', 'year', 'publish_date', 'isactive', 'credit', 'swap']
    list_editable = ['isactive', 'credit']


class Admincomment(admin.ModelAdmin):
    list_display = ['user', 'publishdate']


class Admincontact(admin.ModelAdmin):
    list_display = ['user', 'title', 'contactdate']


class AdminCarAddInfo(admin.ModelAdmin):
    list_display = ['option']


class AdminCarMultipleImages(admin.ModelAdmin):
    # list_display = ['carid']
    pass


class AdminProfile(admin.ModelAdmin):
    list_display = ("user", "phone_number")

admin.site.register(Caradd, Admincar)
admin.site.register(Comment, Admincomment)
admin.site.register(Contact, Admincontact)
admin.site.register(CaraddInfo, AdminCarAddInfo)
admin.site.register(CarMultipleImages, AdminCarMultipleImages)
admin.site.register(Profile, AdminProfile)