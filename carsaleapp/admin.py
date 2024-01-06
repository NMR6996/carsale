from django.contrib import admin
from .models import Caradd, Comment, Contact, CaraddInfo, CarMultipleImages, NewUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ['-date_joined']
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'is_active', 'otp_attempts', 'otp']
    list_editable = ['is_active']
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'otp_attempts', 'otp')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
        }),
    )


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
    list_display = ("user", "phone_number", "otp")
    list_editable = ("otp", )

admin.site.register(Caradd, Admincar)
admin.site.register(Comment, Admincomment)
admin.site.register(Contact, Admincontact)
admin.site.register(CaraddInfo, AdminCarAddInfo)
admin.site.register(CarMultipleImages, AdminCarMultipleImages)
admin.site.register(NewUser, UserAdminConfig)