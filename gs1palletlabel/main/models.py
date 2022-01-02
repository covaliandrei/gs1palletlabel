from django.db import models


class Suppliers(models.Model):
    supplier = models.CharField('supplier', max_length=50)
    supplier_name = models.TextField('Description')

    def __str__(self):
        return self.supplier

    class Meta:
        verbose_name ='Supplier'
        verbose_name_plural = 'Suppliers'

class Destinations(models.Model):
    destination = models.CharField('destination', max_length=150)
    destination_name = models.TextField('DestinationName')

    def __str__(self):
        return self.destination

    class Meta:
        verbose_name ='Destination'
        verbose_name_plural = 'Destinations'
