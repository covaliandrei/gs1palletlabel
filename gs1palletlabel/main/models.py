from django.db import models


class Suppliers(models.Model):
    supplier = models.CharField('supplier', max_length=50)
    supplier_name = models.TextField('Description')

    def __str__(self):
        return self.supplier
