from django.db import models
from posts.models import Post


# Create your models here.
class Image(models.Model):
    imageurl = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
