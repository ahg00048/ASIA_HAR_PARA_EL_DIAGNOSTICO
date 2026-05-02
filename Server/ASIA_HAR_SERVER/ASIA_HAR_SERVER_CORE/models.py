from django.db import models

# Create your models here.
class PatientSensorData(models.Model):
    path = models.CharField(max_length=100) # SOLO EL DIR


class User(models.Model):
    name = models.CharField(db_default="username" ,max_length=100)
    first_name = models.CharField(db_default="first_name" ,max_length=100)
    last_name = models.CharField(db_default="last_name" ,max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(db_default="password", max_length=256)
    admin = models.BooleanField(db_default=False)


class Patient(models.Model):
    first_name = models.CharField(db_default="first_name" ,max_length=100)
    last_name = models.CharField(db_default="last_name" ,max_length=100)
    card_id = models.CharField(max_length=10)
    home_id = models.PositiveIntegerField()
    sensor_data = models.ForeignKey(PatientSensorData, null=True, on_delete=models.SET_NULL)
    users_assigned = models.ManyToManyField(User)
