from django.db import models
from customers.models import Customer
from posts.models import Post


# Create your models here.
class Like(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
