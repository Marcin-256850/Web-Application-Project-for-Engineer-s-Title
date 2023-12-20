from django.contrib import admin
from .models import User, Task, Order, Warehouse, Picture


admin.site.register(User)
admin.site.register(Task)
admin.site.register(Order)
admin.site.register(Warehouse)
admin.site.register(Picture)
