import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError

EXCLUDE_FROM_MIDDLEWARE = ['Django_Rest_Framework.views.apiIndexView',
                            'Django_Rest_Framework.views.IndexView',
                             'costumer.api.views.LoginView',
                             'costumer.api.views.RegisterUserApiView',
                             'store.api.views.ProductApiView',
                             'store.api.views.productDetailAPiView',
                             'store.api.views.CategoryProductApiView',
                             'costumer.api.views.LogoutView'
]

class AuthorizationHeaderMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        if view_name in EXCLUDE_FROM_MIDDLEWARE:
            return None

    def process_template_response(self,request, response):
        try:
            access_token = request.COOKIES[settings.SIMPLE_JWT["AUTH_COOKIE"]]
            refesh_token = request.COOKIES[settings.SIMPLE_JWT["AUTH_COOKIE_REF"]]
            # check if the access token is valid
            # if not, send new access token to cookie
            if access_token:
                key = settings.SECRET_KEY
            else:
                return response
            try:
                decoded_access_token = jwt.decode(access_token, key, algorithms=["HS256"])
                return response
            except jwt.ExpiredSignatureError:
                serializer = TokenRefreshSerializer(data={"refresh":refesh_token})
                try:
                    serializer.is_valid(raise_exception=True)
                except TokenError as e:
                    # Code that is executed in each request after the view is 
                    return response
                
                """ send http only cookies """
                data = serializer._validated_data

                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE_REF"],
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                return response
        except KeyError:
            return response