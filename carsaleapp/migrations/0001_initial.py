# Generated by Django 4.2.3 on 2024-01-04 08:59

import carsaleproject.storage_backends
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='last name')),
                ('phone_number', models.CharField(max_length=7, verbose_name='phone number')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('otp', models.CharField(max_length=4, verbose_name='otp')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Caradd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(blank=True, max_length=9, null=True)),
                ('brand', models.CharField(blank=True, max_length=20, null=True, verbose_name='marka')),
                ('model', models.CharField(blank=True, max_length=23, null=True, verbose_name='model')),
                ('ban', models.CharField(blank=True, max_length=15, null=True, verbose_name='ban növü')),
                ('color', models.CharField(blank=True, max_length=15, null=True, verbose_name='rəng')),
                ('fuel', models.CharField(blank=True, max_length=15, null=True, verbose_name='yanacaq növü')),
                ('transmitter', models.CharField(blank=True, max_length=15, null=True, verbose_name='ötürücü')),
                ('year', models.CharField(blank=True, max_length=4, null=True, verbose_name='buraxılış ili')),
                ('gearbox', models.CharField(blank=True, max_length=20, null=True, verbose_name='ötür')),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='getdiyi yol')),
                ('distanceunit', models.CharField(blank=True, max_length=5, null=True)),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='qiymət')),
                ('priceunit', models.CharField(blank=True, max_length=8, null=True)),
                ('volume', models.IntegerField(blank=True, null=True, verbose_name='mator həcmi')),
                ('power', models.IntegerField(blank=True, null=True, verbose_name='at gücü')),
                ('market', models.CharField(blank=True, max_length=15, null=True, verbose_name='bazar')),
                ('condition', models.CharField(blank=True, max_length=25, null=True, verbose_name='vəziyyəti')),
                ('seats', models.CharField(blank=True, max_length=13, null=True)),
                ('credit', models.CharField(blank=True, max_length=5, null=True)),
                ('swap', models.CharField(blank=True, max_length=5, null=True)),
                ('frontimage', models.ImageField(storage=carsaleproject.storage_backends.PublicMediaStorage(), upload_to='front/')),
                ('sideimage', models.ImageField(storage=carsaleproject.storage_backends.PublicMediaStorage(), upload_to='side/')),
                ('interiorimage', models.ImageField(storage=carsaleproject.storage_backends.PublicMediaStorage(), upload_to='interior/')),
                ('iscomment', models.BooleanField(default=True)),
                ('addinfo', models.TextField(null=True)),
                ('onetimeaddimage', models.BooleanField(default=False)),
                ('isactive', models.BooleanField(default=True)),
                ('publish_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yayınlanma tarixi: ')),
            ],
            options={
                'ordering': ['-publish_date', 'id'],
            },
        ),
        migrations.CreateModel(
            name='CaraddInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('contactdate', models.DateTimeField(auto_now_add=True)),
                ('ischoosingme', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-contactdate',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('publishdate', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='carsaleapp.caradd')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('publishdate',),
            },
        ),
        migrations.CreateModel(
            name='CarMultipleImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='caraddimages/')),
                ('carid', models.ManyToManyField(blank=True, default=None, related_name='carid', to='carsaleapp.caradd')),
            ],
        ),
        migrations.AddField(
            model_name='caradd',
            name='caraddinfo',
            field=models.ManyToManyField(blank=True, default=None, related_name='caraddinfo', to='carsaleapp.caraddinfo'),
        ),
        migrations.AddField(
            model_name='caradd',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='caradd',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
