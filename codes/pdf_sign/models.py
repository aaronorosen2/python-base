from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Doc(models.Model):
    document_id = models.CharField(max_length=64, unique=True, primary_key=True)
    date = models.CharField(max_length=20)
    listing_firm_commission = models.IntegerField(validators=[MaxValueValidator(100)],default=0)
    selling_firm_commission = models.IntegerField(validators=[MaxValueValidator(100)], default=0)
    ref_firm_comm = models.IntegerField(validators=[MaxValueValidator(100)], default=0)
    
    refer_firm = models.CharField(max_length=640)
    ref_broker_name = models.CharField(max_length=100)
    refer_address = models.CharField(max_length=100)
    refer_phone = models.CharField(max_length=17)
    refer_email = models.CharField(max_length=30)
    
    destination_firm = models.CharField(max_length=640)
    dest_broker_name = models.CharField(max_length=100)
    dest_address = models.CharField(max_length=100)
    dest_phone = models.CharField(max_length=17)
    dest_email = models.CharField(max_length=30)
    
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    other = models.CharField(max_length=30,blank=True, null=True)
    pros_name = models.CharField(max_length=50)
    pros_address = models.CharField(max_length=50)
    pros_phone = models.CharField(max_length=50)
    pros_email = models.CharField(max_length=50)
    
    comments = models.TextField()
    months = models.IntegerField(validators=[MaxValueValidator(30)], default=18)
    ref_sign = models.TextField(blank=True, null=True, default='')
    dest_sign = models.TextField(blank=True, null=True,default='')
    
    created_at = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.name