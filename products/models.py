from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    description = models.TextField()
    goal_amount = models.IntegerField()
    closing_date = models.DateTimeField()
    funding_amount = models.IntegerField()