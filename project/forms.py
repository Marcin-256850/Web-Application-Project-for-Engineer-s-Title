from django import forms
from .models import Order, Task, Warehouse


class orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "description", "client", "adress", "state"]
        labels = {
            "name": "Nazwa zamówienia",
            "description": "Opis zamówienia",
            "client": "Nazwa klienta",
            "adress": "Adres klienta",
            "state": "Status zamówienia",
        }


class taskform(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "user", "order", "dates"]
        labels = {
            "name": "Nazwa zadania",
            "user": "Pracownik",
            "order": "Dla zamówienia",
            "dates": "Planowany start wykonywanego zadania",
        }


class warehouseform(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "amount"]
        labels = {
            "name": "Nazwa materiału",
            "amount": "Ilość posiadanego materiału (m²)",
        }


class pricingorder(forms.Form):
    name = forms.CharField(label="Podaj nazwę usługi:")
    amount = forms.IntegerField(label="Podaj ilość:")
    netto = forms.FloatField(label="Podaj wartość netto:")
    vat = forms.FloatField(label="Podaj VAT (procent):")
