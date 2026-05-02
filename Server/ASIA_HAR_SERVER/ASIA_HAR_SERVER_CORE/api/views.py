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
|                        ENPOINTS CORE FUNC                          |
======================================================================
'''

# =========================== Users ===========================

def deleteUser(request, userId):
    try:
        user = User.objects.get(userId)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response()


def addUser(request):
    pass


def modifyUser(request):
    pass


def login(request):
    pass

# =========================== Patients ===========================

def addPatient(request, userId):
    pass


def getPatients(request, userId):
    pass


def removePatient(request, userId, patientId):
    pass


def getPatientData(request, userId, patientId):
    pass


def modifyPatient(request, userId, patientId):
    pass

# =========================== Example Patient Data ===========================

def getExamplePatientData(request, userId, patientId):
    pass

'''
======================================================================
|                      ENPOINTS WRAPPER FUNCS                        |
======================================================================
'''

# =========================== Users ===========================

@api_view(['GET', 'POST'])
def User_Get_Or_Create(request):
    if request.method == 'GET':
        login(request)
    elif request.method == 'POST':
        addUser(request)


@api_view(['PUT', 'DELETE'])
def User_Delete_Or_Modify(request, id):
    if request.method == 'PUT':
        modifyUser(request, id)
    elif request.method == 'DELETE':
        deleteUser(request, id)

# =========================== Patients ===========================

@api_view(['GET', 'POST'])
def Patients_Get_All_Or_Add(request, id):
    if request.method == 'GET':
        getPatients(request, id)
    elif request.method == 'POST':
        addPatient(request, id)


@api_view(['GET', 'DELETE', 'PUT'])
def Patients_Get_SensorData_Or_Delete_Or_Add_Or_Modify(request, userId, patientId):
    if request.method == 'GET':
        getPatientData(request, userId, patientId)
    elif request.method == 'DELETE':
        removePatient(request, userId, patientId)
    elif request.method == 'PUT':
        modifyPatient(request, userId, patientId)

# ============== BASIC / JUST TO RESUME DESKTOP DEV ==============

@api_view(['GET'])
def Get_Example_Patient_Data(request, userEmail, patientId):
    pass
    