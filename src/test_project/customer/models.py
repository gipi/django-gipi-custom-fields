from django.db import models
from django import forms
from django.contrib import admin
from django_gipi_custom_fields import DatiBancariModelField, DatiBancariFormField

# Create your models here.
class Customer(models.Model):
        Name = models.CharField(max_length=50)
        DatiBancari = DatiBancariModelField()

class CustomerForm(forms.ModelForm):
        class Meta:
                model = Customer

        DatiBancari = DatiBancariFormField()

class CustomerAdmin(admin.ModelAdmin):
        form = CustomerForm

admin.site.register(Customer, CustomerAdmin)
