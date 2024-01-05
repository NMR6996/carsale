from .forms import NewComment, NewContactUs
from .models import Caradd, CarMultipleImages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .custom_functions import *
import random
from django.urls import reverse


@csrf_exempt
def register_request(request):
    message = random.randint(1000, 9999)
    if request.method == 'POST':
        username = (request.POST["username"]).lower()
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        phone_number = request.POST["phone_number"]

        if pass1 == pass2:
            if NewUser.objects.filter(username=username).exists():
                messages.error(request, "Bu ad artıq istifadə olunub!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
            else:
                if NewUser.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, "Bu telefon nömrəsi artıq istifadə olunub!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
                else:
                    if len(pass1) < 6:
                        messages.error(request, "Parol minimum 6 simvoldan ibarət olmalıdır!")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
                    else:
                        if len(phone_number) != 12:
                            messages.error(request, "Telefon nömrəsini düzgün daxil edin!")
                            messages.error(request, "Nümunə: 994709924546")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
                        else:
                            user = NewUser.objects.create_user(username=username, phone_number=phone_number, password=pass1, is_active=False, otp=message)
                            user.save()
                            send_otp(phone_number, message)

                            messages.success(request, "Qeydiyyatınız uğurla tamamlandı!")
                            messages.success(request,
                                             "Hesabı aktivləşdirmək üçün bir dəfəlik parolu daxil edin!)")
                            return redirect('otp', username=username, phone_number=phone_number)
        else:
            messages.error(request, "Parollar eyni deyil!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
    return render(request, "signup/register.html")


def on_time_password(request, username, phone_number):
    if request.method == "POST":
        otp = request.POST["otp"]
        try:
            user = NewUser.objects.get(username=username, phone_number=phone_number, otp=otp)
            user.is_active = True
            user.otp_attempts -= 1
            user.save()
            messages.success(request, "Hesabınız aktivləşdirildi!")
            return redirect('login')
        except NewUser.DoesNotExist:
            messages.error(request, "Bir dəfəlik parolu düzgün daxil edin! ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, "signup/otp.html")


@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username və ya password səhvdir!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
    return render(request, 'signup/login.html')


def logout_request(request):
    logout(request)
    return redirect("home")


def forget_password_request(request):
    if request.method == 'POST':
        username = request.POST["username"]
        try:
            user = NewUser.objects.get(username=username)
            message = random.randint(1000, 9999)
            user.otp = message
            user.save()
            send_otp(user.phone_number, message)
            messages.success(request, "Birdəfəlik parol telefonunuza göndərildi!")
            return redirect('reset-password', username=username)

        except NewUser.DoesNotExist:
            messages.error(request, "Bu adda hesab tapılmadı!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'signup/forget-password.html')


def reset_password_request(request, username):
    user = NewUser.objects.get(username=username)
    if request.method == 'POST':
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        otp = request.POST["otp"]
        if otp == user.otp and password1 == password2:
            if len(password1) >= 6:
                user.set_password(password1)
                user.save()
                messages.success(request, "Parolunuz uğurla dəyişdirildi")
                return redirect('login')
            else:
                messages.error(request, "Parol minimum 6 simvoldan ibarət olmalıdır!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif otp != user.otp and password1 == password2:
            messages.error(request, "Bir dəfəlik parolu düzgün daxil edin!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif otp == user.otp and password1 != password2:
            messages.error(request, "Parollar eyni deyil!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Daxil etdiyiniz məlumatlarda səhvlik var!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'signup/reset-password.html')


@csrf_exempt
def contact(request):

    if request.method == 'POST':
        contact_form = NewContactUs(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            return render(request, "contact.html", {"success": "İstəyiniz uğurla qeydə alındı!"})

    return render(request, "contact.html")


def profile(request):
    user = NewUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()
        messages.success(request, "Parolunuz uğurla dəyişdirildi")
        return render(request, "profile.html", {"user": user})
    return render(request, "profile.html", {"user": user})


@csrf_exempt
@login_required(login_url="login")
def caradd(request):
    if request.method == 'POST':
        usage = request.POST["usage"]
        brand = request.POST["brand"]
        model = request.POST["model"]
        ban = request.POST["ban"]
        color = request.POST["color"]
        fuel = request.POST["fuel"]
        transmitter = request.POST["transmitter"]
        year = request.POST["year"]
        gearbox = request.POST["gearbox"]
        mileage = request.POST["mileage"]
        distanceunit = request.POST["distanceunit"]
        price = request.POST["price"]
        priceunit = request.POST["priceunit"]
        volume = request.POST["volume"]
        power = request.POST["power"]
        market = request.POST["market"]
        condition = request.POST["condition"]
        seats = request.POST["seats"]
        credit = request.POST["credit"]
        swap = request.POST["swap"]
        front = request.FILES.get('front')
        side = request.FILES.get('side')
        interior = request.FILES.get('interior')
        iscomment = request.POST["iscomment"]
        addinfo = request.POST["addinfo"]
        add_list = request.POST.getlist("addlist")
        new_car = Caradd(
            user=request.user,
            usage=usage,
            brand=brand,
            model=model,
            ban=ban,
            color=color,
            fuel=fuel,
            transmitter=transmitter,
            gearbox=gearbox,
            mileage=mileage,
            distanceunit=distanceunit,
            price=price,
            priceunit=priceunit,
            year=year,
            volume=volume,
            power=power,
            market=market,
            condition=condition,
            seats=seats,
            credit=credit,
            swap=swap,
            frontimage=front,
            sideimage=side,
            interiorimage=interior,
            iscomment=iscomment,
            addinfo=addinfo
        )
        new_car.save()
        for i in add_list:
            new_car.caraddinfo.add(i)
        new_car.save()
        return render(request, "cars/caradd.html", {"success": "Elanınız uğurla dərc edildi! "})
    return render(request, "cars/caradd.html")


def car_detailed_views(request, id):
    car = get_object_or_404(Caradd, id=id)
    context = {"car": car}

    # car comments view
    comments = car.comments.all()
    if request.method == 'POST':
        comment_form = NewComment(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.car = car
            user_comment.save()
            return HttpResponseRedirect('/car_details/' + str(car.id), context)
    else:
        comment_form = NewComment()
    return render(request, "cars/car-details.html", {
        'comments': comments,
        'comments_form': comment_form,
        "car": car,
        "carimages": CarMultipleImages.objects.filter(carid=car.id)
    })


def carviews(request):
    cars = Caradd.objects.filter(isactive=True)
    carpaginator = Paginator(cars, 6)
    page = request.GET.get('page')
    try:
        cars = carpaginator.page(page)
    except PageNotAnInteger:
        cars = carpaginator.page(1)
    except EmptyPage:
        cars = carpaginator.page(carpaginator.num_pages)

    return render(request, "cars/cars.html", {"cars": cars})


@csrf_exempt
def searchcar(request):
    if request.method == 'POST':
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        pricemin = request.POST.get("minPrice")
        pricemax = request.POST.get("maxPrice")
        yearmin = request.POST.get("minYear")
        yearmax = request.POST.get("maxYear")

        cars = Caradd.objects.all()

        # Add filters based on provided parameters
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if model:
            cars = cars.filter(model__icontains=model)
        if pricemin:
            cars = cars.filter(price__gte=pricemin)
        if pricemax:
            cars = cars.filter(price__lte=pricemax)
        if yearmin:
            cars = cars.filter(year__gte=yearmin)
        if yearmax:
            cars = cars.filter(year__lte=yearmax)

        if (brand == '' and model == '' and pricemin == '' and pricemax == '' and yearmax == '' and yearmin == '') or not cars.exists():
            warning = 'Axtarışa uyğun heçnə tapılmadı!'

            return render(request, "cars/searchcar.html", {"warning": warning})
        return render(request, "cars/searchcar.html", {'cars': cars})
    return render(request, "cars/searchcar.html")


def favorites_add(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.favorites.filter(id=request.user.id).exists():
        car.favorites.remove(request.user)
    else:
        car.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url="login")
def favorites_list(request):
    cars = Caradd.objects.filter(favorites=request.user)
    carpaginator = Paginator(cars, 6)
    page = request.GET.get('page')
    try:
        cars = carpaginator.page(page)
    except PageNotAnInteger:
        cars = carpaginator.page(1)
    except EmptyPage:
        cars = carpaginator.page(carpaginator.num_pages)
    return render(request, "cars/favorites.html", {"cars": cars})


@login_required(login_url='login')
def carads_list(request):
    cars = Caradd.objects.filter(user=request.user)
    carpaginator = Paginator(cars, 6)
    page = request.GET.get('page')
    try:
        cars = carpaginator.page(page)
    except PageNotAnInteger:
        cars = carpaginator.page(1)
    except EmptyPage:
        cars = carpaginator.page(carpaginator.num_pages)
    return render(request, "cars/elanlar.html", {"cars": cars})


@csrf_exempt
def carads_remove(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.user.id == request.user.id:
        car.delete()
    return redirect("elanlar")


@csrf_exempt
def carcomment_add(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.user.id == request.user.id:
        if car.iscomment:
            car.iscomment = False
            car.save()
        else:
            car.iscomment = True
            car.save()
    return HttpResponseRedirect('/car_details/' + str(car.id))


@login_required(login_url='login')
def careditviews(request, id):
    car = get_object_or_404(Caradd, id=id)

    if request.method == 'POST':
        usage = request.POST["usage"]
        brand = request.POST["brand"]
        model = request.POST["model"]
        ban = request.POST["ban"]
        color = request.POST["color"]
        fuel = request.POST["fuel"]
        transmitter = request.POST["transmitter"]
        year = request.POST["year"]
        gearbox = request.POST["gearbox"]
        mileage = request.POST["mileage"]
        distanceunit = request.POST["distanceunit"]
        price = request.POST["price"]
        priceunit = request.POST["priceunit"]
        volume = request.POST["volume"]
        power = request.POST["power"]
        market = request.POST["market"]
        condition = request.POST["condition"]
        seats = request.POST["seats"]
        credit = request.POST["credit"]
        swap = request.POST["swap"]
        images = request.FILES.getlist('images')
        addinfo = request.POST["addinfo"]

        for image in images:
            if len(images) > 15:
                return render(request, 'cars/caredit.html', {'car': car,
                                                        'error': f'Siz maksimum 15 şəkil əlavə edə bilərsiniz. Seçdiyiniz şəkil sayı: {len(images)}'})
            else:
                carimages = CarMultipleImages.objects.create(images=image)
                carimages.carid.add(car.id)
                car.onetimeaddimage = True

        car.usage = usage
        car.brand = brand
        car.model = model
        car.ban = ban
        car.color = color
        car.fuel = fuel
        car.transmitter = transmitter
        car.year = year
        car.gearbox = gearbox
        car.mileage = mileage
        car.distanceunit = distanceunit
        car.price = price
        car.priceunit = priceunit
        car.volume = volume
        car.power = power
        car.market = market
        car.condition = condition
        car.seats = seats
        car.credit = credit
        car.swap = swap
        car.addinfo = addinfo
        car.save()
        return render(request, 'cars/caredit.html', {'car': car, 'success': 'Uğurla redakte olundu'})

    return render(request, 'cars/caredit.html', {'car': car})
