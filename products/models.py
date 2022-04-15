from django.db import models
from users.models import User
import datetime

# Create your models here.

class Product(models.Model):
    
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    title = models.CharField(max_length=30)
    description = models.TextField()
    goal_amount = models.IntegerField()
    closing_date = models.DateField()
    onetime_funding_amount = models.IntegerField()
    total_funding_amount = models.IntegerField(default=0)
    
    publisher = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    supporter = models.ManyToManyField("users.User")
    
    def supporter_count(self):
        return self.supporter.count()
    
    def d_day(self):
        now = datetime.date.today()
        spplit = list(map(int,str(self.closing_date).split("-")))
        target_day = datetime.date(spplit[0],spplit[1],spplit[2])
        values = target_day - now
        return values.days
        
        
    