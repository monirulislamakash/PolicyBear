from django.db import models
import datetime 
from tinymce.models import HTMLField
# Create your models here.
class Blog(models.Model):
    Name=models.CharField(max_length=350)
    Image=models.FileField(upload_to="BlogImage/")
    Description=HTMLField()
    readtime=models.CharField(max_length=20,default='5 min read')
    Date=models.DateField(default=datetime.datetime.today())

class Frequently_Asked_Question(models.Model):
    Question=models.CharField(max_length=300)
    Answer=HTMLField()

class Privacy_Policy(models.Model):
    Privacy_Policy=HTMLField()
    Date=models.DateField(default=datetime.datetime.today())

class Terms_of_Service(models.Model):
    Terms_of_Service=HTMLField()
    Date=models.DateField(default=datetime.datetime.today())

class Disclaimer(models.Model):
    Disclaimer=HTMLField()
    Date=models.DateField(default=datetime.datetime.today())




#==============================>
# Job Post ====================>
#==============================>
class CareersCategory(models.Model):
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.category
class CareersLocation(models.Model):
    Location=models.CharField(max_length=100)
    def __str__(self):
        return self.Location

class CareersJobType(models.Model):
    Job_Type=models.CharField(max_length=100)
    def __str__(self):
        return self.Job_Type
class CareersDepartment(models.Model):
    Department=models.CharField(max_length=100)
    def __str__(self):
        return self.Department

class JobPost(models.Model):
    Titel=models.CharField(max_length=100)
    vacancy=models.CharField(max_length=100)
    Experience=models.CharField(max_length=100)
    Department=models.ForeignKey(CareersDepartment,on_delete=models.CASCADE)
    Location=models.ForeignKey(CareersLocation,on_delete=models.CASCADE)
    JobType=models.ForeignKey(CareersJobType,on_delete=models.CASCADE)
    SalaryRange=models.CharField(max_length=100)  
    category=models.ForeignKey(CareersCategory,on_delete=models.CASCADE)
    PostDate=models.DateField(default=datetime.datetime.today())
    short_description=models.TextField()
    description=HTMLField()

class AppliedCandidates(models.Model):
    Position=models.CharField(max_length=100)
    Full_Name=models.CharField(max_length=100)
    Phone=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    CV=models.FileField(upload_to="Candidates_CV/")
    Cover_Letter=models.TextField()
    Application_Date=models.DateField(default=datetime.datetime.today())


# APIs Model
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
    AgeFrom=models.IntegerField()
    AgeTo=models.IntegerField()
    IncomeFrom=models.IntegerField()
    IncomeTO=models.IntegerField()