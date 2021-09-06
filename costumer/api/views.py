import json
from store.api.serializers import ProductCreateSerializer, ProductEditSerializer
from utils.rawQuery import dictfetchall
from costumer.models import Location, Store, TokenNotif
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from django.db import connections

from datetime import datetime, timedelta
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework.views import APIView
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
    StoreOrdersSerializers,
    StoreProductsSerializers,
    TokenSerializer,
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
        qs = Store.objects.get(pemilik=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_queryset(), context={"date": request.GET.get("date")}
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StoreOrderApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    serializer_class = StoreOrdersSerializers

    def get_queryset(self):
        qs = Store.objects.get(pemilik=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search", False)
        serializer = self.get_serializer(
            self.get_queryset(),
            context={"search": search, "page": request.GET.get("page", 1)},
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StoreProductAPiView(GenericAPIView, CreateModelMixin):
    permission_classes = [IsAuthenticated, isOwner]

    def get_serializer_class(self):
        return (
            ProductCreateSerializer
            if self.request.method == "POST"
            else StoreProductsSerializers
        )

    def get_queryset(self):
        qs = Store.objects.get(pemilik=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_queryset(),
            context={"page": request.GET.get("page", 1)},
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        store = Store.objects.get(pemilik=self.request.user)
        serializer.save(penjual=store)


class WhoamiApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        data = WhoamiSerializer(self.get_queryset()).data
        return Response(data)


class TokenApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenSerializer

    def get_queryset(self):
        return TokenNotif.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class LocationDatailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()

    def get_serializer_class(self):
        if self.request.method != "GET":
            return LocationEditSerializer
        return LocationSerializer


class LocationIndo(APIView):
    __db = connections["provinces"].cursor()
    queryset = None

    def execSql(self, query):
        cursor = self.__db
        # Data modifying operation - commit required
        cursor.execute(query)
        return dictfetchall(cursor)


class AddressIndoApiView(LocationIndo):
    def sortPostalCode(self, query):
        data = {}
        for item in query:
            name = f"{item['city']}_{item['sub_district']}"

            if name in data:
                data[name] = [*data[name], item["postal_code"]]
            else:
                data[name] = [item["postal_code"]]
        return data

    def mergeData(self, data, postal_code):
        new_data = []
        for item in data:
            name = f"{item['city']}_{item['sub_district']}"
            if name in postal_code:
                new_data.append({**item, "postal_code": postal_code[name]})
        return new_data

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search", False)

        if search:
            query = f'SELECT DISTINCT Province.province_name ,Address.sub_district,Address.city,Address.city_id FROM db_postal_code_data as Address JOIN db_province_data as Province ON Province.province_code=Address.province_code  WHERE city LIKE "%{search}%" OR sub_district LIKE "%{search}%" '
            query_code = f'SELECT DISTINCT Address.city,Address.sub_district,Address.postal_code FROM db_postal_code_data as Address JOIN db_province_data as Province ON Province.province_code=Address.province_code  WHERE city LIKE "%{search}%" OR sub_district LIKE "%{search}%" ORDER BY Address.postal_code '
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        postal_code = self.sortPostalCode(self.execSql(query_code))
        data = self.mergeData(self.execSql(query), postal_code)

        return Response(data)


class CekOngkir(APIView):
    def post(self, request, *args, **kwargs):
        import requests

        url = "https://api.rajaongkir.com/starter/cost"
        payload = {
            "weight": "100",
            "courier": "jne",
        }
        payload = {**payload, **request.data}
        files = []
        headers = {"key": "597f52e05a00c744d13ff6957a8ee156"}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )
        return Response(json.loads(response.text))
