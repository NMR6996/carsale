from django.db import models
from django.contrib.auth.models import User
from carsaleproject.storage_backends import PublicMediaStorage

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):
    def create_user(self, username, phone_number, password, **extra_fields):
        if not username:
            raise ValueError(_('Username daxil etməlisiniz! '))

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superistifadəçi üçün is_staff aktiv olmalıdır!'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superistifadəçi üçün is_superuser aktiv olmalıdır!'))

        return self.create_user(username, first_name, password, **extra_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=50, unique=True)
    first_name = models.CharField(_('Adınız'), max_length=50, blank=True)
    last_name = models.CharField(_('Soyadınız'), max_length=50, blank=True)
    phone_number = models.CharField(_('Telefon nömrəsi'), max_length=12)
    date_joined = models.DateTimeField(_("Qoşulma tarixi"), default=timezone.now)
    is_staff = models.BooleanField(_("İşçi statusu"), default=False)
    is_active = models.BooleanField(_("Hesab aktivlik statusu"), default=True)
    otp = models.CharField(_('Bir dəfəlik parol'), max_length=4)
    otp_attempts = models.PositiveIntegerField(default=3)

    objects = CustomManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


class CaraddInfo(models.Model):
    option = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.option}"


class Caradd(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    usage = models.CharField(max_length=9, blank=True, null=True)
    brand = models.CharField(verbose_name="marka", max_length=20, blank=True, null=True)
    model = models.CharField(verbose_name="model", max_length=23, blank=True, null=True)
    ban = models.CharField(verbose_name="ban növü", max_length=15, blank=True, null=True)
    color = models.CharField(verbose_name="rəng", max_length=15, blank=True, null=True)
    fuel = models.CharField(verbose_name="yanacaq növü", max_length=15, blank=True, null=True)
    transmitter = models.CharField(verbose_name="ötürücü", max_length=15, blank=True, null=True)
    year = models.CharField(verbose_name="buraxılış ili", max_length=4, null=True, blank=True)
    gearbox = models.CharField(verbose_name="ötür", max_length=20, blank=True, null=True)
    mileage = models.IntegerField(verbose_name="getdiyi yol", null=True, blank=True)
    distanceunit = models.CharField(max_length=5, null=True, blank=True)
    price = models.IntegerField(verbose_name="qiymət", null=True, blank=True)
    priceunit = models.CharField(max_length=8, null=True, blank=True)
    volume = models.IntegerField(verbose_name="mator həcmi", null=True, blank=True)
    power = models.IntegerField(verbose_name="at gücü", null=True, blank=True)
    market = models.CharField(verbose_name="bazar", max_length=15, blank=True, null=True)
    condition = models.CharField(verbose_name="vəziyyəti", max_length=25, blank=True, null=True)
    seats = models.CharField(max_length=13, blank=True, null=True)
    credit = models.CharField(max_length=5, null=True, blank=True)
    swap = models.CharField(max_length=5, null=True, blank=True)
    frontimage = models.ImageField(storage=PublicMediaStorage(), upload_to="front/")
    sideimage = models.ImageField(storage=PublicMediaStorage(), upload_to="side/")
    interiorimage = models.ImageField(storage=PublicMediaStorage(), upload_to="interior/")
    iscomment = models.BooleanField(default=True)
    addinfo = models.TextField(null=True)
    onetimeaddimage = models.BooleanField(default=False)
    isactive = models.BooleanField(default=True)
    caraddinfo = models.ManyToManyField(CaraddInfo, related_name="caraddinfo", default=None, blank=True)
    publish_date = models.DateTimeField(verbose_name="Yayınlanma tarixi: ", auto_now_add=True, null=True)
    favorites = models.ManyToManyField(NewUser, related_name="favorites", default=None, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['-publish_date', 'id']


class CarMultipleImages(models.Model):
    carid = models.ManyToManyField(Caradd, related_name='carid', default=None, blank=True)
    images = models.FileField(upload_to='caraddimages/')

    def __str__(self):
        return f"{self.carid}"


class Comment(models.Model):
    car = models.ForeignKey(Caradd, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    content = models.TextField()
    publishdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("publishdate",)

    def __str__(self):
        return f"{self.user}"


class Contact(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    contactdate = models.DateTimeField(auto_now_add=True)
    ischoosingme = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ("-contactdate",)
