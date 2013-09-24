from django.db import models

# Create your models here.


class Customer(models.Model):
    username = models.CharField(max_length=200)

    token = models.CharField(max_length=200)
    expireds = models.DateTimeField()
    refresh_token = models.CharField(max_length=200)
    
    customer_info = models.TextField(blank=True, null=True)
