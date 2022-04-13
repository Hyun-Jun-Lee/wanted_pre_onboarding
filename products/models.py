from django.db import models
from users.models import User

# Create your models here.

class Product(models.Model):
    
    title = models.CharField(max_length=30)
    description = models.TextField()
    goal_amount = models.IntegerField()
    closing_date = models.DateTimeField()
    funding_amount = models.IntegerField()
    
    publisher = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    