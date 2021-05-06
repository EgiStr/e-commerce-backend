from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    registeruser
)

""" create jwt token manualy """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

""" create jwt http only """
class LoginView(CreateAPIView):
    def post(self, request, format=None):
        response = Response()     

        # authenticate user     
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_active:
                """ create token and send http only cookies """
                data = get_tokens_for_user(user)
                response.set_cookie(
                                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                                    value = data["access"],
                                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                        )
                response.data = {"message" : " Login successfully ","data":data}
                
                return response
            else:
                return Response({"No active" : "This account is not active!!"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"},status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(CreateAPIView):
    def post(self,request, format=None):
        #  check token refresh valid
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response()     
        """ send http only cookies """
        data = serializer._validated_data
        payload = {
            'access':data['access'],
            "refresh":data['refresh']
        }
        response.set_cookie(
                            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                            value = data["access"],
                            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )
        response.data = {"Messege" : "refresh Success",'data':payload}
        response.status_code = status.HTTP_200_OK   
        return response
        
        

class LogoutView(CreateAPIView):
    def post(self,request, format=None):
        """ remove http only """
        response = Response()        
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.data = {
            'Messege':'logout Success'
        }
        response.status_code = status.HTTP_200_OK
        return response

class RegisterUserApiView(CreateAPIView):
    queryset = None
    serializer_class = registeruser
    permission_classes = [AllowAny]


class DashbordView(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        respond = {
            'message':'success'
        }
        return Response(respond,status=status.HTTP_200_OK)