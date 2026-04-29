from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# models and serializers
from ASIA_HAR_SERVER_CORE.models import User
from ASIA_HAR_SERVER_CORE.models import Patient
from ASIA_HAR_SERVER_CORE.api.serializer import UserSerializer
from ASIA_HAR_SERVER_CORE.api.serializer import PatientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PatientSerializer


'''
======================================================================
|                      ENPOINTS WRAPPER FUNCS                        |
======================================================================
'''

# =========================== Users ===========================

@api_view(['GET', 'POST'])
def User_Get_Or_Create(request):
    pass


@api_view(['DELETE', 'PUT'])
def User_Delete_Or_Modify(request, userEmail):
    pass

# =========================== Patients ===========================

@api_view(['GET', 'POST'])
def Patient_Get_All_From_User(request, userEmail):
    pass


@api_view(['GET', 'DELETE', 'PUT'])
def Patients_Get_SensorData_Or_Delete_Or_Add_Or_Modify(request, userEmail, patientId):
    pass


'''
======================================================================
|                        ENPOINTS CORE FUNC                          |
======================================================================
'''


def deleteUser(request, userToDelEmail):
    try:
        user = User.objects.get(email=userToDelEmail)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response()


def addUser(request):
    pass


def login(request):
    pass


def addPatient(request, userEmail):
    pass


def getPatients(request, userEmail):
    pass


def removePatient(request, userEmail, patientId):
    pass


def getPatientData(request, userEmail, patientId):
    pass