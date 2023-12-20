from django.shortcuts import render, redirect
from .models import User, Order, Task, Warehouse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .forms import orderform, taskform, pricingorder, warehouseform
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import random
import io


def user_login(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        passw = request.POST.get("pass")
        user = authenticate(request, email=mail, password=passw)
        if user is not None:
            u = User.objects.get(email=mail)
            request.session["name"] = u.first_name
            request.session["surname"] = u.last_name
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"blad": "Wprowadź poprawne dane."})
    else:
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def user_register(request):
    if request.method == "POST":
        rname = request.POST.get("name")
        rsurname = request.POST.get("surname")
        rmail = request.POST.get("mail")
        rpassword = request.POST.get("pass")
        repass = request.POST.get("repass")
        if rpassword == repass:
            try:
                worker = User(
                    first_name=rname,
                    last_name=rsurname,
                    email=rmail,
                    password=rpassword,
                    username=rname.lower(),
                )
                worker.save()
                send_mail(
                    subject="Pomyślna rejestracja w aplikacji woodlock",
                    message="Gratulujemy pomyślnej rejestracji\nTwoje dane:\nImię:"
                    + rname
                    + "\nNazwisko:"
                    + rsurname
                    + "\nHasło:"
                    + rpassword,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[rmail],
                )
                return render(
                    request,
                    "register.html",
                    {"udane": "Rejestracaj pomyślna możesz przejść do logowania."},
                )
            except:
                return render(
                    request,
                    "register.html",
                    {
                        "blad": "Błąd podczas rejestracji. Spróbuj ponownie.",
                        "form": "form",
                    },
                )
        else:
            return render(request, "register.html", {"blad": "Hasła nie zgadzają się"})
    return render(request, "register.html", {"form": "form"})


def pass_reset_mail(request):
    if request.method == "POST":
        email = request.POST.get("mail")
        try:
            User.objects.get(email=email)
            code = str(random.randrange(100000, 999999))
            request.session["rightmail"] = email
            request.session["code"] = code
            send_mail(
                subject="Zmiana hasła aplikacja dla stolarni",
                message="Kod potrzebny do zmiany hasła: " + code,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return redirect("pass_reset_code")
        except User.DoesNotExist:
            return render(
                request,
                "pass_reset_mail.html",
                {"blad": "Nie ma takiego użytkownika"},
            )
    return render(request, "pass_reset_mail.html")


def pass_reset_code(request):
    rightmail = request.session.get("rightmail", None)
    code = request.session.get("code", None)
    if request.method == "POST":
        u = User.objects.get(email=rightmail)
        passw = request.POST.get("pass")
        repassw = request.POST.get("repass")
        recode = request.POST.get("code")
        if passw == repassw and code == recode:
            u.password = passw
            u.save()
            request.session.clear()
            return render(
                request, "pass_reset_code.html", {"udane": "Zmiana hasła udała się"}
            )
        else:
            return render(
                request,
                "pass_reset_code.html",
                {"blad": "Kod lub hasła nie zgadzają się", "code": "code"},
            )
    return render(request, "pass_reset_code.html", {"code": "code"})


def home(request):
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    if role == "wl" or role == "kr":
        return render(request, "home.html", {"permission": "yes", "info": info})
    else:
        return render(request, "home.html", {"info": info})


def orders(request):
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    if request.method == "GET":
        order = Order.objects.all()
        if role == "wl" or role == "kr":
            return render(
                request,
                "orders.html",
                {"permission": "yes", "info": info, "orders": order},
            )
        else:
            return render(request, "orders.html", {"info": info, "orders": order})


def createorder(request):
    if request.method == "POST":
        form = orderform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("orders")
        else:
            return render(
                request,
                "createorder.html",
                {
                    "permission": "yes",
                    "info": info,
                    "form": form,
                    "blad": "Niepoprawne dane.Spróbuj ponownie",
                },
            )
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    form = orderform()
    if role == "wl" or role == "kr":
        return render(
            request,
            "createorder.html",
            {"permission": "yes", "info": info, "form": form},
        )
    else:
        return render(request, "createorder.html", {"info": info})


def updateorder(request, pk):
    info = request.user.first_name + " " + request.user.last_name
    order = Order.objects.get(id=pk)
    form = orderform(instance=order)
    context = {"permission": "yes", "info": info, "form": form}
    if request.method == "POST":
        form = orderform(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders")

    return render(request, "updateorder.html", context)


def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect("orders")


def tasks(request):
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    current_date = datetime.now()
    week = "Obecny"
    if request.method == "POST":
        if "previousweek" in request.POST:
            current_date -= timedelta(weeks=1)
            week = "Poprzedni"
        elif "nextweek" in request.POST:
            current_date += timedelta(weeks=1)
            week = "Przyszły"
        elif "currentweek" in request.POST:
            current_date = datetime.now()
            week = "Obecny"

    pon, wt, sr, czw, pt, sun = calculateweek(current_date)
    if role == "wl" or role == "kr":
        mon_task = Task.objects.filter(dates__date=pon)
        tues_task = Task.objects.filter(dates__date=wt)
        wedn_task = Task.objects.filter(dates__date=sr)
        thurs_task = Task.objects.filter(dates__date=czw)
        frid_task = Task.objects.filter(dates__date=pt)
        context = {
            "info": info,
            "pon": pon,
            "sun": sun,
            "mon_task": mon_task,
            "tues_task": tues_task,
            "wedn_task": wedn_task,
            "thurs_task": thurs_task,
            "frid_task": frid_task,
            "week": week,
        }
        context["permission"] = "yes"
        return render(
            request,
            "tasks.html",
            context,
        )
    else:
        id = request.user.id
        mon_task = Task.objects.filter(dates__date=pon).filter(user=id)
        tues_task = Task.objects.filter(dates__date=wt).filter(user=id)
        wedn_task = Task.objects.filter(dates__date=sr).filter(user=id)
        thurs_task = Task.objects.filter(dates__date=czw).filter(user=id)
        frid_task = Task.objects.filter(dates__date=pt).filter(user=id)
        context = {
            "info": info,
            "pon": pon,
            "sun": sun,
            "mon_task": mon_task,
            "tues_task": tues_task,
            "wedn_task": wedn_task,
            "thurs_task": thurs_task,
            "frid_task": frid_task,
            "week": week,
        }
        return render(
            request,
            "tasks.html",
            context,
        )


def calculateweek(target_date):
    pon = target_date - timedelta(days=target_date.weekday())
    wt = pon + timedelta(days=1)
    sr = pon + timedelta(days=2)
    czw = pon + timedelta(days=3)
    pt = pon + timedelta(days=4)
    sun = pon + timedelta(days=6)
    pon_formatted = pon.strftime("%Y-%m-%d")
    wt_formatted = wt.strftime("%Y-%m-%d")
    sr_formatted = sr.strftime("%Y-%m-%d")
    czw_formatted = czw.strftime("%Y-%m-%d")
    pt_formatted = pt.strftime("%Y-%m-%d")
    sun_formatted = sun.strftime("%Y-%m-%d")
    return (
        pon_formatted,
        wt_formatted,
        sr_formatted,
        czw_formatted,
        pt_formatted,
        sun_formatted,
    )


def createtask(request):
    info = request.user.first_name + " " + request.user.last_name
    form = taskform()
    if request.method == "POST":
        form = taskform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks")
        else:
            context = {
                "permission": "yes",
                "info": info,
                "form": form,
                "blad": "Niepoprawne dane",
            }
            return render(request, "createtask.html", context)
    else:
        context = {"permission": "yes", "info": info, "form": form}
        return render(request, "createtask.html", context)


def updatetask(request, pk):
    info = request.user.first_name + " " + request.user.last_name
    task = Task.objects.get(id=pk)
    form = taskform(instance=task)
    context = {"permission": "yes", "info": info, "form": form}
    if request.method == "POST":
        form = taskform(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks")
    return render(request, "updatetask.html", context)


def deletetask(request, pk):
    order = Task.objects.get(id=pk)
    order.delete()
    return redirect("tasks")


def price(request):
    info = request.user.first_name + " " + request.user.last_name
    if request.method == "GET":
        order = Order.objects.filter(Q(state="wc") | Q(state="zk"))
        return render(
            request, "price.html", {"permission": "yes", "info": info, "orders": order}
        )


def priceorder(request, pk):
    info = request.user.first_name + " " + request.user.last_name
    request.session["pk"] = pk
    form = pricingorder()
    if request.method == "POST":
        if "clear" in request.POST:
            request.session.pop("service_list", None)
            return render(
                request,
                "priceorder.html",
                {
                    "permission": "yes",
                    "info": info,
                    "form": form,
                },
            )
        else:
            form = pricingorder(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                amount = form.cleaned_data["amount"]
                netto = form.cleaned_data["netto"]
                vat = form.cleaned_data["vat"]
                service_list = request.session.get("service_list", [])
                service_list.append([name, amount, netto, vat])
                request.session["service_list"] = service_list
                return render(
                    request,
                    "priceorder.html",
                    {
                        "permission": "yes",
                        "info": info,
                        "form": form,
                        "list": service_list,
                    },
                )
            else:
                return render(
                    request,
                    "priceorder.html",
                    {
                        "permission": "yes",
                        "info": info,
                        "form": form,
                        "blad": "Błędne dane",
                    },
                )
    else:
        return render(
            request,
            "priceorder.html",
            {"permission": "yes", "info": info, "form": form},
        )


def saveprice(request, pk):
    order = Order.objects.get(id=pk)
    service_list = request.session.get("service_list", [])
    sumnetto = 0
    sumvat = 0
    sum = 0
    for service in service_list:
        sumnetto = sumnetto + service[2]
        sumvat = sumvat + service[2] * (service[3] / 100)
    sum = sum + sumnetto + sumvat
    request.session.pop("service_list", None)
    order.assessed = sum
    order.state = "wc"
    order.save()
    return redirect("price")


def generatepriceorder(request, pk):
    order = Order.objects.get(id=pk)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    title = "Faktura nr " + str(order.id)
    p.setTitle(title)
    # Wysokośc to 850 a Szerokość 600 to pierwszy argument to szerokość potem wysokość1
    p.drawInlineImage(
        "C:/Users/kamil/Desktop/web_app/static/img/background.jpg", 50, 750, 100, 50
    )
    p.drawString(250, 725, "Faktura nr " + str(order.id))
    p.drawString(50, 700, "Nabywaca")
    p.drawString(50, 685, "Nazwa:" + order.client)
    p.drawString(50, 670, "Adres:" + order.adress)
    p.drawString(400, 700, "Data wystawienia: " + str(date.today()))
    p.drawString(
        400, 685, "Termin platnosci: " + str(date.today() + timedelta(weeks=2))
    )
    data = [["NAZWA USLUGI/ TOWARU", "ILOSC", "WARTOSC NETTO", "VAT"]]
    service_list = request.session.get("service_list", [])
    for service in service_list:
        data.append(service)
    t = Table(
        data,
        style=[
            ("BOX", (0, 0), (3, 0), 1, colors.gray),
            ("BACKGROUND", (0, 0), (3, 0), colors.gray),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
        ],
    )
    t.wrapOn(p, 0, 0)
    t.drawOn(p, 150, 500)
    sumnetto = 0
    sumvat = 0
    sum = 0
    for service in service_list:
        sumnetto = sumnetto + service[2]
        sumvat = sumvat + service[2] * (service[3] / 100)
    sum = sumvat + sumnetto
    p.drawString(400, 200, "Wartosc Netto: " + str(sumnetto) + " zl")
    p.drawString(400, 185, "Vat: " + str(sumvat) + " zl")
    p.drawString(400, 170, "Razem do zaplaty: " + str(sum) + " zl")
    p.drawString(50, 115, "Frima Woodlock")
    p.line(30, 111, 570, 111)
    p.drawString(50, 100, "ul Franciszka 12 Kalisz")
    p.drawString(50, 85, "NIP:72631713623")
    p.drawString(400, 100, "Forma platnosci: przelew")
    p.drawString(400, 85, "Bank: Santander")
    p.drawString(400, 70, "Numer konta bankowego:")
    p.drawString(400, 55, "6459852908390842")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename="Faktura nr " + str(order.id) + ".pdf"
    )


def editpriceorder(request, pk):
    info = request.user.first_name + " " + request.user.last_name
    if request.method == "GET":
        order = Order.objects.filter(Q(state="wc") | Q(state="zk"))
        return render(
            request, "price.html", {"permission": "yes", "info": info, "orders": order}
        )


def warehouse(request):
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    materials = Warehouse.objects.all()
    if role == "wl" or role == "kr":
        return render(
            request,
            "warehouse.html",
            {"permission": "yes", "info": info, "materials": materials},
        )
    else:
        return render(request, "warehouse.html", {"info": info, "materials": materials})


def createwarehouse(request):
    role = request.user.role
    info = request.user.first_name + " " + request.user.last_name
    form = warehouseform()
    if request.method == "POST":
        form = warehouseform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("warehouse")
        else:
            return render(
                request,
                "createwarehouse.html",
                {
                    "permission": "yes",
                    "info": info,
                    "form": form,
                    "blad": "Niepoprawne dane.Spróbuj ponownie",
                },
            )
    return render(
        request,
        "createwarehouse.html",
        {"permission": "yes", "info": info, "form": form},
    )


def updatewarehouse(request, pk):
    info = request.user.first_name + " " + request.user.last_name
    warehouse = Warehouse.objects.get(id=pk)
    form = warehouseform(instance=warehouse)
    context = {"permission": "yes", "info": info, "form": form}
    if request.method == "POST":
        form = warehouseform(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect("warehouse")

    return render(request, "updatewarehouse.html", context)


def deletewarehouse(request, pk):
    warehouse = Warehouse.objects.get(id=pk)
    warehouse.delete()
    return redirect("warehouse")
