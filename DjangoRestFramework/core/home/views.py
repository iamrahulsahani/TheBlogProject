from functools import partial
from django.shortcuts import render
from rest_framework.decorators import api_view, APIView, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer, LoginSerializer, RegisterSerializer

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['GET', "POST"])
def index(request, usr):
    if request.method == "POST":
        print(request.data)
        msg = "data posted..."
        return Response(msg)
    elif request.method == "GET":
        data = {
            'course':'python',
            'content' : ['flask', 'django' , 'fastapi'],
            'author' : 'rahul'
        }
        print(type(usr))
        return Response(data)

@api_view(['GET', 'POST', "PUT", "PATCH", 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def people(request):
    if request.method == "GET":
        out = Person.objects.all()
        serializer = PersonSerializer(out, many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PUT":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "DELETE":
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
            obj.delete()
            return Response({"msg":"data deleted..."})
        except:
            return Response({"msg":"data not found..."}, status=404)


#for full CRUD operation
class PeopleViewSets(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message':serializer.errors
            }, status=400)

        serializer.save()
        return Response({'status':True, 'msg':'user created !'}, status=201)

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message':serializer.errors
            }, status=400)

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message':'Invalid Creds'
            }, status=400)


        token = Token.objects.create(user=user)

        return Response({'status':True, 'token':str(token),'msg':'user logged in !'}, status=200)


    

    


