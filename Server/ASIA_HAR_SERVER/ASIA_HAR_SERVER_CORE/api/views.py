from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


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

def deleteUser(request, userId): # Body -> current user | query param -> email of user to del
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if (not user.admin and user.email != request.query_params.get('email_to_del')):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        userToDel = User.objects.get(email=request.query_params.get('email_to_del'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    userToDel.delete()
    
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response(status=status.HTTP_200_OK)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


def addUser(request): # Body -> current user 
    # check if user is created properly (password checks etc)

    #
    if User.objects.filter(email=request.data.get('email')).count() != 0:
        return Response(status=status.HTTP_409_CONFLICT) 

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def modifyUser(request, userId): # Body -> current user 
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check password

    #

    serializer = UserSerializer(user, data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


def login(request): # query param -> email and password
    try:
        user = User.objects.get(email=request.query_params.get('email'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    password = request.query_params.get('password')
    
    if not check_password(password, user.password):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

# =========================== Patients ===========================

def addPatient(request, userId):
    return Response(status=status.HTTP_404_NOT_FOUND)


def getPatients(request, userId):
    return Response(status=status.HTTP_404_NOT_FOUND)


def removePatient(request, userId, patientId):
    return Response(status=status.HTTP_404_NOT_FOUND)


def getPatientData(request, userId, patientId):
    return Response(status=status.HTTP_404_NOT_FOUND)


def modifyPatient(request, userId, patientId):
    return Response(status=status.HTTP_404_NOT_FOUND)

# =========================== Example Patient Data ===========================

def getExamplePatientData(request, userId, patientId):
    return Response(status=status.HTTP_404_NOT_FOUND)


'''
======================================================================
|                      ENPOINTS WRAPPER FUNCS                        |
======================================================================
'''

# =========================== Users ===========================

@api_view(['GET', 'POST'])
def User_Get_Or_Create(request, format=None):
    if request.method == 'GET':
        return login(request)
    elif request.method == 'POST':
        return addUser(request)


@api_view(['PUT', 'DELETE'])
def User_Delete_Or_Modify(request, userId, format=None):
    if request.method == 'PUT':
        return modifyUser(request, userId)
    elif request.method == 'DELETE':
        return deleteUser(request, userId)

# =========================== Patients ===========================

@api_view(['GET', 'POST'])
def Patients_Get_All_Or_Add(request, userId, format=None):
    if request.method == 'GET':
        return getPatients(request, userId)
    elif request.method == 'POST':
        return addPatient(request, userId)


@api_view(['GET', 'DELETE', 'PUT'])
def Patients_Get_SensorData_Or_Delete_Or_Add_Or_Modify(request, userId, patientId, format=None):
    if request.method == 'GET':
        return getPatientData(request, userId, patientId)
    elif request.method == 'DELETE':
        return removePatient(request, userId, patientId)
    elif request.method == 'PUT':
        return modifyPatient(request, userId, patientId)

# ============== BASIC / JUST TO RESUME DESKTOP DEV ==============

@api_view(['GET'])
def Get_Example_Patient_Data(request, format=None):
    return getExamplePatientData()
    