from django.contrib import admin

from .models import User, Patient

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    model = Patient