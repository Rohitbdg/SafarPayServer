from __future__ import unicode_literals

from django.db import models

# Create your models here.
class users(models.Model):
    user_id=models.CharField(max_length=30,unique=True,primary_key=True,editable=False)
    password=models.CharField(max_length=30)
    Name=models.CharField(max_length=40)
    Mobile=models.CharField(max_length=10)
    Address=models.CharField(max_length=100,blank=True)
    email=models.EmailField(max_length=20,blank=True)
    rto_balance=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.user_id + " " +self.Name
    def getname(self):
        return self.Name

    def deduct_amt(self,amt):
        self.rto_balance=self.rto_balance-amt
        self.save()

    def getvehicles(self):
        #get count
        n=len(self.vehicles_set.all())
        listd=[]
        for i in range(0,n):
            listd.append(str(self.vehicles_set.all()[i]))
        return listd

    def add_amt(self,amt):
        print amt
        self.rto_balance=self.rto_balance+int(amt)
        self.save()



class toll(models.Model):
    toll_id=models.PositiveIntegerField(primary_key=True,unique=True)
    toll_name=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    latitude=models.FloatField()
    longitude=models.FloatField()
    services=models.PositiveIntegerField()
    car_price=models.PositiveIntegerField(blank=False)
    bike_price=models.PositiveIntegerField(blank=False)
    bus_price=models.PositiveIntegerField(blank=False)
    truck_price=models.PositiveIntegerField(blank=False)
    def __str__(self):
        return str(self.toll_id) + " " +self.toll_name







class vehicles(models.Model):
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    vehicle_no=models.CharField(max_length=10,unique=True,primary_key=True)
    vehicle_type=models.PositiveIntegerField(blank=False)
    special_vehicle=models.BooleanField(default=False)
    def __str__(self):
        return  self.vehicle_no

    def checkno(self,number):
        if self.user_id.user_id==number:
            return True
        return False
