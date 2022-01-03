from django.db import models


class Suppliers(models.Model):
    supplier = models.CharField('supplier', max_length=50)
    supplier_name = models.TextField('Description')

    def __str__(self):
        return self.supplier

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class Destinations(models.Model):
    destination = models.CharField('destination', max_length=150)
    destination_name = models.TextField('DestinationName')

    def __str__(self):
        return self.destination

    class Meta:
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'


class Products(models.Model):
    product_name = models.CharField('ProductName', max_length=250)
    product_scu = models.CharField('ProductSCU', max_length=16)
    boxes_per_pallet = models.SmallIntegerField('BoxesPerPallet')
    weight_brutto = models.CharField('WeightBrutto', max_length=8)
    weight_netto = models.CharField('WeightNetto', max_length=8)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Labels(models.Model):
    order_number = models.CharField('OrderNumber', max_length=25)
    supplier_id = models.ForeignKey(Suppliers, null=True, on_delete= models.SET_NULL)
    destination_id = models.ForeignKey(Destinations, null=True, on_delete= models.SET_NULL)
    pallets_count = models.SmallIntegerField('PalletsCount')
    product_id = models.ForeignKey(Products, null=True, on_delete= models.SET_NULL)
    link_to_pdf = models.CharField('LinkToPdf', max_length=500)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'