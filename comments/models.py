from django.db import models
from customers.models import Customer
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField()
    status = models.IntegerField(default=1)
