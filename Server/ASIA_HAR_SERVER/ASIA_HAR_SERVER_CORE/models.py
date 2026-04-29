from django.db import models

# Create your models here.
class PatientSensorData(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=100)


class Patient(models.Model):
    first_name = models.CharField(db_default="first_name" ,max_length=100)
    last_name = models.CharField(db_default="last_name" ,max_length=100)
    idCard = models.CharField(primary_key=True, max_length=10)
    homeId = models.PositiveIntegerField()
    sensorData = models.ForeignKey(PatientSensorData, null=True, on_delete=models.SET_NULL)


class User(models.Model):
    name = models.CharField(db_default="username" ,max_length=100)
    first_name = models.CharField(db_default="first_name" ,max_length=100)
    last_name = models.CharField(db_default="last_name" ,max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(db_default="password", max_length=256)
    admin = models.BooleanField(db_default=False)
    patientsAssigned = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)