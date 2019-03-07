from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Incident(models.Model):
    STATUS = (
        ('Reported', 'Reported'),
        ('Handling', 'Handling'),
        ('Closed', 'Closed'),
    )
    LEVEL = (
        ('CAT1', 'CAT1'),
        ('CAT2', 'CAT2')
    )
    REGION = (
        ('Central Region', 'Central Region'),
        ('East Region', 'East Region'),
        ('North Region', 'North Region'),
        ('North-East Region', 'North-East Region'),
        ('West Region', 'West Region')
    )
    INCIDENT_TYPE = (
        ('Dengue Outbreak', 'Dengue Outbreak'),
        ('Terrorist', 'Terrorist'),
        ('Haze', 'Haze')
    )

    incident_type= models.CharField(max_length=100, choices=INCIDENT_TYPE)
    managedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    region = models.CharField(max_length=100, choices=REGION)
    status = models.CharField(max_length=100, choices=STATUS)
    level = models.CharField(max_length=100, choices=LEVEL)

class Report(models.Model):
    incident =  models.ForeignKey(Incident, on_delete=models.CASCADE)
    reporterFirstName = models.CharField(max_length=100, default='')
    reporterLastName = models.CharField(max_length=100, default='')
    phoneNumber = models.IntegerField()
    description = models.TextField()

class Assistance(models.Model):
    ASSISTANCE_TYPE = (
        ('Emergency Ambulance', 'Emergency Ambulance'),
        ('Rescue and Evacuation', 'Rescue and Evacuation'),
        ('Fire-Fighting', 'Fire-Fighting'),
        ('Gas Leak Control', 'Gas Leak Control')
    )
    incident = models.ForeignKey(Report, on_delete=models.CASCADE)
    assistanceType = models.CharField(max_length=100, choices=ASSISTANCE_TYPE)

class PublicSubcriber(models.Model):
    REGION = (
        ('Central Region', 'Central Region'),
        ('East Region', 'East Region'),
        ('North Region', 'North Region'),
        ('North-East Region', 'North-East Region'),
        ('West Region', 'West Region')
    )
    phoneNumber = models.IntegerField(unique=True)
    region = models.CharField(max_length=100, choices=REGION)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()

class GovernmentAgent(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.IntegerField(unique=True)