from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    WORKER = "pr"
    MANAGER = "kr"
    OWNER = "wl"

    options = [
        (WORKER, "pracownik"),
        (MANAGER, "kierownik"),
        (OWNER, "wlasciciel"),
    ]

    role = models.CharField(
        max_length=10,
        choices=options,
        default=WORKER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Picture(models.Model):
    path = models.ImageField


class Order(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    client = models.CharField(max_length=30)
    adress = models.CharField(max_length=100)
    PENDING = "tw"
    FINISHED = "zk"
    PRICED = "wc"
    LIST = [
        (PENDING, "W trakcie"),
        (FINISHED, "zakonczony"),
        (PRICED, "wyceniony"),
    ]
    state = models.CharField(
        max_length=10,
        choices=LIST,
        default=PENDING,
    )
    assessed = models.FloatField(null=True)
    order = models.OneToOneField(Picture, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    dates = models.DateTimeField(null=False)
    datef = models.DateTimeField(null=True)
    waste = models.FloatField(null=True)


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    amount = models.FloatField(default=0)
