from django.urls import path
from . import views


urlpatterns = [
    path("", views.user_login, name="login"),
    path("", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("pass_reset_mail/", views.pass_reset_mail, name="pass_reset_mail"),
    path("pass_reset_code/", views.pass_reset_code, name="pass_reset_code"),
    path("home/", views.home, name="home"),
    path("orders/", views.orders, name="orders"),
    path("createorder/", views.createorder, name="createorder"),
    path("updateorder/<str:pk>", views.updateorder, name="updateorder"),
    path("deleteorder/<str:pk>", views.deleteorder, name="deleteorder"),
    path("tasks/", views.tasks, name="tasks"),
    path("createtask/", views.createtask, name="createtask"),
    path("updatetask/<str:pk>", views.updatetask, name="updatetask"),
    path("deletetask/<str:pk>", views.deletetask, name="deletetask"),
    path("warehouse/", views.warehouse, name="warehouse"),
    path("price/", views.price, name="price"),
    path("priceorder/<str:pk>", views.priceorder, name="priceorder"),
    path(
        "generaterpriceorder/<str:pk>",
        views.generatepriceorder,
        name="generatepriceorder",
    ),
    path(
        "saveprice/<str:pk>",
        views.saveprice,
        name="saveprice",
    ),
    path("createwarehouse/", views.createwarehouse, name="createwarehouse"),
    path("updatewarehouse/<str:pk>", views.updatewarehouse, name="updatewarehouse"),
    path("deletewarehouse/<str:pk>", views.deletewarehouse, name="deletewarehouse"),
]
