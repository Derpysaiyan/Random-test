from django.db import models

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    experience = models.TextField()
    goals = models.TextField()



class Availability(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)#delete if model is deleted
    days = models.TextField()
    times = models.TextField()
