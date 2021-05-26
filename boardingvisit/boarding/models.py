from django.db import models
from django.core.exceptions import ValidationError

class Dateinyear(models.Model):
    date = models.DateField()    
    is_weekend = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    weight = models.IntegerField(default=1)


class Dog(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    def __str__(self):
            return self.first_name + " " + self.last_name

class Visit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_at = models.DateField()
    end_at = models.DateField()

    def clean(self):
        
        if self.start_at > self.end_at:
            raise ValidationError("Dates are incorrect")

    
    