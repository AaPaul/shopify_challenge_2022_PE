from operator import mod
from django.db import models

# Create your models here.
class City(models.Model):
    tnt = "TORONTO"
    ott = "OTTAWA"
    kan = "KANATA"
    ny = "NEW YORK"
    van = "VANCOUVER"
    city_choices = [
        ("TORONTO", tnt),
        ("OTTAWA", ott),
        ("KANATA", kan),
        ("NEW YORK", ny),
        ("VANCOUVER", van)
    ]
    name = models.CharField(max_length=50, choices=city_choices, unique=True)


class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    
        


class Inventory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.DO_NOTHING, null=True, blank=True)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.RESTRICT, null=False, blank=False)



