from django.db import models

# Create your models here.
class PatientSensorData(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=100)


class Patient(models.Model):
    name = models.CharField(max_length=100)
    idCard = models.CharField(primary_key=True, max_length=10)
    homeId = models.PositiveIntegerField()
    sensorData = models.ForeignKey(PatientSensorData, on_delete=models.CASCADE)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True, max_length=100)
    password = models.CharField(max_length=255)
    patientsAssigned = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)