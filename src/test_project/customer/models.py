from django.db import models
from django import forms
from django.contrib import admin
from django_gipi_custom_fields import DatiBancariModelField, DatiBancariFormField, OrariModelField
from django_gipi_custom_fields.forms import OrariFormField

# Create your models here.
class Customer(models.Model):
        Name = models.CharField(max_length=50)
        DatiBancari = DatiBancariModelField()

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Name', 'DatiBancari')

class Shop(models.Model):
        name = models.CharField(max_length=50)
        orari = OrariModelField()

class ShopForm(forms.ModelForm):
        class Meta:
            model = Shop

        orari = OrariFormField()

class ShopAdmin(admin.ModelAdmin):
        form = ShopForm

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Shop, ShopAdmin)
