from .forms import NewComment, NewContactUs, EditUserProfile
from .models import Caradd, CarMultipleImages, Profile
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from smtplib import SMTPRecipientsRefused
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def send_activation_mail(user, request):
    current_site = get_current_site(request)
    email_subject = 'Hesab aktivasiyası'
    email_body = render_to_string('activation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


@csrf_exempt
def reset_password_mail(user, request):
    current_site = get_current_site(request)
    email_subject = 'Parol sıfırlama'
    email_body = render_to_string('resetting.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


@csrf_exempt
def register_request(request):
    if request.method == 'POST':
        username = (request.POST["username"]).lower()
        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        mobile = request.POST["phone_number"]

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html",
                              {
                                  "error": "Bu ad artıq istifadə olunub!",
                                  "username": username,
                                  "email": email
                              })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "register.html",
                                  {
                                      "error": "Bu e-poçt artıq istifadə olunub!",
                                      "username": username,
                                      "email": email
                                  })
                else:
                    if Profile.objects.filter(phone_number=mobile).exists():
                            return render(request, "register.html",
                                {
                                    "error":"Bu telefon nömrəsi artıq istifadə olunub!",
                                    "username":username,
                                    "mobile":mobile,
                                    "email":email
                                })
                    else:
                        if len(pass1) < 6:
                            return render(request, "register.html", {
                                "error": "Parol minimum 6 simvoldan ibarət olmalıdır! ",
                                "username": username,
                                "mobile": mobile,
                                "email": email
                            })
                        else:
                            if len(mobile) != 10:
                                return render(request, "register.html", {
                                    "error": "Telefon nömrəsini düzgün daxil edin: nümunə: 0501112233 ",
                                    "username": username,
                                    "mobile": mobile,
                                    "email": email
                                })
                            else:
                                user = User.objects.create_user(username=username, email=email,
                                                                password=pass1)
                                user.is_active = False
                                user.save()
                                profile = Profile(user=user, phone_number=mobile)
                                profile.save()

                                # mail gonder
                                try:
                                    send_activation_mail(user, request)
                                except SMTPRecipientsRefused:
                                    user.delete()
                                    return render(request, "register.html", {
                                        "error": "E-poçtunuzu düzgün daxil etməsəniz, qeydiyyatınız tamamlanmayacaq! ",
                                        "username": username,
                                        "mobile": mobile,
                                        "email": email
                                    })

                                return render(request, "login.html",
                                              {
                                                  "success1": "Qeydiyyatınız uğurla tamamlandı!",
                                                  "success2": "Hesabı aktivləşdirmək üçün e-poçta daxil olun.(Spam "
                                                              "bölməsinə baxın!)",
                                                  "username": username,
                                              })
        else:
            return render(request, "register.html",
                          {
                              "error": "Parollar eyni deyil!",
                              "username": username,
                              "email": email
                          })
    return render(request, "register.html")


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
            return render(request, "login.html", {
                "error": "Daxil edilən məlumatlarda səhvlik var!"
            })
    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    return redirect("home")


def activate_user(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'login.html',
                      {"success1": 'Email aktivləşdirildi giriş edə bilərsiniz.', 'username': user})
    else:
        return render(request, 'login.html', {"success1": 'Email aktivdir', 'username': user})


@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not User.objects.filter(username=username).first():
            return render(request, "forget-password.html",
                          {'message': 'Belə username tapılmadı:', 'username': username})
        user = User.objects.get(username=username)
        reset_password_mail(user, request)
        return render(request, 'login.html', {'message': 'E-poçtunuza parol sıfırlmaq linki göndərildi!'})
    return render(request, 'forget-password.html')


@csrf_exempt
def reset_password(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    user_id = user.id

    if user and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            pass1 = request.POST["password1"]
            pass2 = request.POST["password2"]
            user_id = request.POST["user_id"]
            if pass1 != pass2:
                messages.warning(request, 'Parollar eyni deyil!')
                return redirect(f'/reset-password/{uidb64}/{token}')
            else:
                if len(pass1) < 6:
                    messages.warning(request, "Parol minimum 6 simvoldan ibarət olmalıdır! ")
                    return redirect(f'/reset-password/{uidb64}/{token}')

                else:
                    user = User.objects.get(id=int(user_id))
                    user.set_password(pass1)
                    user.save()
                    return render(request, 'login.html',
                                  {'success1': "Parolunuz uğurla dəyişdirildi!", 'username': user.username})

    return render(request, 'reset-password.html', {'user_id': user_id})


@csrf_exempt
def contact(request):

    if request.method == 'POST':
        contact_form = NewContactUs(request.POST)

        if contact_form.is_valid():
            contact_form.save()
            return render(request, "contact.html", {"success": "İstəyiniz uğurla qeydə alındı!"})

    return render(request, "contact.html")


def profile(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']

        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile.phone_number = phone_number
        profile.save()

        return render(request, "profile.html", {
            "user": user,
            "profile": profile,
            "success": "Uğurla redakte olundu!"
        })
    return render(request, "profile.html", {
        "user": user,
        "profile": profile
    })

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
        return render(request, "caradd.html", {"success": "Elanınız uğurla dərc edildi! "})
    return render(request, "caradd.html")


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
    return render(request, "car-details.html", {
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

    return render(request, "cars.html", {"cars": cars})


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

            return render(request, "searchcar.html", {"warning": warning})
        return render(request, "searchcar.html", {'cars': cars})
    return render(request, "searchcar.html")


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
    return render(request, "favorites.html", {"cars": cars})


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
    return render(request, "elanlar.html", {"cars": cars})


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
                return render(request, 'caredit.html', {'car': car,
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
        return render(request, 'caredit.html', {'car': car, 'success': 'Uğurla redakte olundu'})

    return render(request, 'caredit.html', {'car': car})
