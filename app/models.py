from django.db import models
# Create your models here.
class State(models.Model):
    state=models.CharField(max_length=50)
    def __str__(self):
        return self.state

class Carrier(models.Model):
    carrier=models.CharField(max_length=50)
    def __str__(self):
        return self.carrier

class Our_Partner_And_Location(models.Model):
    Carrier=models.ForeignKey(Carrier,on_delete=models.CASCADE)
    State=models.ForeignKey(State,on_delete=models.CASCADE)
    Payout=models.CharField(max_length=50)

class SecondaryOffer(models.Model):
    State=models.ForeignKey(State,on_delete=models.CASCADE)
    Carrier=models.ForeignKey(Carrier,on_delete=models.CASCADE)
    PolicyPlan=models.CharField(max_length=50)
    AgeFrom=models.IntegerField(max_length=50)
    AgeTo=models.IntegerField(max_length=50)
    IncomeFrom=models.IntegerField(max_length=50)
    IncomeTO=models.IntegerField(max_length=50)