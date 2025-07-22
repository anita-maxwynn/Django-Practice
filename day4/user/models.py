from django.db import models

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.roll}"
    
class Result(models.Model):
    stu_class = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.stu_class} - {self.marks}"
