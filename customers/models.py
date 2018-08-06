from django.db import models


# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=25)
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    info = models.CharField(max_length=300)
    address = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='images/')
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.username
