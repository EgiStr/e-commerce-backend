from costumer.models import Location, Store
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from datetime import datetime, timedelta
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


from .permission import isAuthor, isOwner
from .serializers import (
    ChangePasswordSerializer,
    LocationCreateSerializer,
    LocationEditSerializer,
    LocationSerializer,
    StoreDetailSerializers,
    WhoamiSerializer,
    registeruser,
    UserDetailSerilaizer,
    UserEditProfilSerializer,
)

User = get_user_model()

""" create jwt token manualy """


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


""" create jwt http only """


class ChangePasswordApiView(UpdateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.data.get("new_password") != serializer.data.get(
                "new_password2"
            ):
                return Response(
                    {"new_password": ["didnt macth"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(
            {"password new": ["password new wrong. doesnt macth"]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        response = Response()

        # authenticate user
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                """create token and send http only cookies"""
                data = get_tokens_for_user(user)

                tomorrow = datetime.now() + timedelta(days=7)
                expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=expires,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE_REF"],
                    value=data["refresh"],
                    expires=expires,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.data = {"message": " Login successfully "}

                return response
            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid username or password!!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefreshTokenView(APIView):
    def post(self, request, format=None):
        #  check token refresh valid
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response()
        """ send http only cookies """
        data = serializer._validated_data

        payload = {"access": data["access"], "refresh": data["refresh"]}
        tomorrow = datetime.now() + datetime.timedelta(days=1)
        expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=data["access"],
            expires=expires,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.data = {"Messege": "refresh Success", "data": payload}
        response.status_code = status.HTTP_200_OK
        return response


class LogoutView(APIView):
    def post(self, request, format=None):
        """remove http only"""
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REF"])
        response.data = {"Messege": "logout Success"}
        response.status_code = status.HTTP_200_OK
        return response


class RegisterUserApiView(CreateAPIView):
    queryset = None
    serializer_class = registeruser
    permission_classes = [AllowAny]


class DashbordView(UpdateModelMixin, GenericAPIView):

    permission_classes = [isAuthor, IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method != "GET":
            return UserEditProfilSerializer
        return UserDetailSerilaizer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    def get(self, request):

        data = UserDetailSerilaizer(self.get_queryset()).data
        return Response(data)

    # delete user / not active user !
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REF"])
        response.data = {
            "message": f"success Remove user {user.email}, GoobBye Friends "
        }
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StoreDashboardApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    serializer_class = StoreDetailSerializers

    def get_queryset(self):
        return Store.objects.get(pemilik=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class WhoamiApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        data = WhoamiSerializer(self.get_queryset()).data
        return Response(data)


class LocationApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method != "GET":
            return LocationCreateSerializer
        return LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)


class LocationDatailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    def get_serializer_class(self):
        if self.request.method != "GET":
            return LocationEditSerializer
        return LocationSerializer
    
