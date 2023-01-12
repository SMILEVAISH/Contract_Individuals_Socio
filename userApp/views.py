from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.hashers import make_password

from core import settings

import random

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

from userApp.models import CustomUser
from userApp.serializers import UserSerializer, LoginSerializer
from userApp.mixins import otp_email, generate_otp


# Create your views here.
'''
User Detail
'''
class UserDetails(APIView):
    def get(self, request, id):
        qs = CustomUser.objects.filter(id = id)
        ser = UserSerializer(qs, many = True)
        return Response(
            {
                'data' : ser.data
            }
        )


'''
User Registerations
'''
class Register(GenericAPIView):

    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        
        serializer.save()  # add this line
        return Response({
            'message': 'Successfully Registered'
        })


'''
All Users
'''
class AllUsers(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    
    def get(self, request):
        qs = CustomUser.objects.all()
        ser = UserSerializer(qs, many=True)
        data = list(ser.data)
        print('this is ',type(data))
        print(data)
        return Response(data)


'''
Login Using Password
'''
class PasswordLogin(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Get the otp
                # otp_generated = serializer.data['otp_generated']
                otp = request.session.get('otp')
                if otp is not None:
                # Verify the otp
                    if otp == request.session.get('otp'):
                        login(request, user)
                        return Response({'message' : 'Log in Successfull'},status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response({'message': 'Otp Did not match'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Generating the otp and saving in the session
                    otp = generate_otp()
                    print(otp,': this is a generated otp for the session')
                    request.session['otp'] = otp
                    # sending mail to the user
                    otp_email.delay(email, otp)
                    return Response({'message': f'Otp sent successfully to your mail : {email}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'message':'Email or Password is Wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
Log out 
'''
class LogOutApi(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    def post(self,request):
        logout(request)
        return Response({"success": "Successfully logged out."})