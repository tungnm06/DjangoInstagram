from django.db import models
from customers.models import Customer
# Create your models here.


class Post(models.Model):
    content = models.TextField()
    likes = models.IntegerField(default=1)
    commends = models.IntegerField(default=0)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField()
    status = models.IntegerField(default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
