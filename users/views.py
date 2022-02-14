from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from users.serializers import UserSerializer
from .models import User
import jwt ,datetime

# Create your views here.

class RegisterView(APIView):
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        payload = {
            "id":user.id,
            "exp" :datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "iat" : datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        # tokenValue = jwt.decode(token,'secret',algorithms=['HS256'])
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }
        return response
        
        
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not Found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        
        payload = {
            "id":user.id,
            "exp" :datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "iat" : datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload,'secret',algorithm='HS256')
        # tokenValue = jwt.decode(token,'secret',algorithms=['HS256'])
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }
        return response
    
class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id = payload['id']).first()
        
        serializer = UserSerializer(user)
            
        return Response(serializer.data)

class UpdateView(APIView):
    
    def put(self,request):
        # first get the id of the user from jwt token
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        # email = request.data['email']
        
        # user = User.objects.filter(email=email).first()
        user = User.objects.filter(id = payload['id']).first()
        serializer = UserSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data ={
            'msg' : 'success'
        }           
        return response
    
    
class DeleteView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        

        u = User.objects.filter(id = payload['id']).first()
        u.delete()       
   
        response = Response()
        response.delete_cookie('jwt')
        response.data ={
            'msg' : 'success'
        }           
        return response
