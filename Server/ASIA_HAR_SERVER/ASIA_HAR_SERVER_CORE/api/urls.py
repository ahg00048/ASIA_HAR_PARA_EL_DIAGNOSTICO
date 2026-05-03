from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ASIA_HAR_SERVER_CORE.api import views

urlpatterns = [
    path('users/', views.User_Get_Or_Create),
    path('users/<int:userId>/', views.User_Delete_Or_Modify),
    path('users/<int:userId>/patients', views.Patients_Get_All_Or_Add),
    path('users/<int:userId>/patients/<int:patientId>/', views.Patients_Get_SensorData_Or_Delete_Or_Add_Or_Modify),
    
    path('example/', views.Get_Example_Patient_Data),
]

urlpatterns = format_suffix_patterns(urlpatterns)