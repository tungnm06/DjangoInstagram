from django.db import models
from customers.models import Customer
from posts.models import Post

# Create your models here.

class Notification(models.Model):
    customer_id = models.IntegerField()
    customer_user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField()
    createtime = models.DateTimeField()
    status = models.IntegerField()
