from django.db import models
import datetime

class Products(models.Model):
    product_name=models.CharField(max_length=50)
    purchase_date=models.DateField(default=datetime.date.today)
    expiry_date=models.DateField(default=datetime.date.today)
    photo=models.ImageField(upload_to="",default="default.png")
    expires_in=models.IntegerField(default=0)
    vendor_email=models.EmailField(default="",max_length=50)
    vendor_name=models.CharField(max_length=50)
    payment_mode=models.CharField(max_length=50,default="")

    def __str__(self):
        return self.product_name

class Certificates(models.Model):
    domain_name=models.CharField(max_length=50)
    purchase_date=models.DateField(default=datetime.date.today)
    expiry_date=models.DateField(default=datetime.date.today)
    photo=models.ImageField(upload_to="",default="default.png")
    expires_in=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    auto_renew = models.IntegerField(default= 0)

    def __str__(self):
        return self.domain_name


class Subscribe(models.Model):
    email=models.EmailField(default="",max_length=50)
    status=models.IntegerField(default= 0)

    def __str__(self):
        return self.email
