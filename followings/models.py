from django.db import models
from customers.models import Customer

# Create your models here.

class Follow(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer')
    cusdetail = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='cusdetail')
    status = models.IntegerField(default=1)
