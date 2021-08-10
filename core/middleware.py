import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError

EXCLUDE_FROM_MIDDLEWARE = [
    "Django_Rest_Framework.views.apiIndexView",
    "Django_Rest_Framework.views.IndexView",
    "costumer.api.views.LoginView",
    "costumer.api.views.RegisterUserApiView",
    "store.api.views.ProductApiView",
    "store.api.views.productDetailAPiView",
    "store.api.views.CategoryProductApiView",
    "costumer.api.views.LogoutView",
]


class AuthorizationHeaderMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = ".".join((view_func.__module__, view_func.__name__))
        if view_name in EXCLUDE_FROM_MIDDLEWARE:
            return None

    def process_template_response(self, request, response):
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
                decoded_access_token = jwt.decode(
                    access_token, key, algorithms=["HS256"]
                )
                return response
            except jwt.ExpiredSignatureError:
                serializer = TokenRefreshSerializer(data={"refresh": refesh_token})
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


import logging
import re
from django.db import connection
import os

logger = logging.getLogger(__name__)


def sql_logger():
    print("TOTAL QUERIES: " + str(len(connection.queries)))
    print("TOTAL TIME: " + str(sum([float(q["time"]) for q in connection.queries])))
    print("INDIVIDUAL QUERIES:")
    # logger.debug('TOTAL QUERIES: ' + str(len(connection.queries)))
    # logger.debug('TOTAL TIME: ' + str(sum([float(q['time']) for q in connection.queries])))

    # logger.debug('INDIVIDUAL QUERIES:')
    for i, query in enumerate(connection.queries):
        sql = re.split(
            r"(SELECT|FROM|WHERE|GROUP BY|ORDER BY|INNER JOIN|LIMIT)", query["sql"]
        )
        if not sql[0]:
            sql = sql[1:]
        sql = [(" " if i % 2 else "") + x for i, x in enumerate(sql)]
        # print('\n### {} ({} seconds)\n\n{};\n'.format(i, query['time'], '\n'.join(sql)))
        # logger.debug('\n### {} ({} seconds)\n\n{};\n'.format(i, query['time'], '\n'.join(sql)))


def terminal_width():
    """
    Function to compute the terminal width.
    """
    width = 0
    try:
        import struct, fcntl, termios

        s = struct.pack("HHHH", 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack("HHHH", x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ["COLUMNS"])
        except:
            pass
    if width <= 0:
        width = 80
    return width


def SqlPrintingMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if (
            not settings.DEBUG
            or len(connection.queries) == 0
            or request.path_info.startswith(settings.MEDIA_URL)
            or "/admin/jsi18n/" in request.path_info
        ):
            return response

        indentation = 2
        print(
            "\n\n%s\033[1;35m[SQL Queries for]\033[1;34m %s\033[0m\n"
            % (" " * indentation, request.path_info)
        )
        width = terminal_width()
        total_time = 0.0
        for query in connection.queries:
            nice_sql = query["sql"].replace('"', "").replace(",", ", ")
            sql = "\033[1;31m[%s]\033[0m %s" % (query["time"], nice_sql)
            total_time = total_time + float(query["time"])
            while len(sql) > width - indentation:
                print("%s%s" % (" " * indentation, sql[: width - indentation]))
                sql = sql[width - indentation :]
            print("%s%s\n" % (" " * indentation, sql))
        replace_tuple = (" " * indentation, str(total_time))
        print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
        print(
            "%s\033[1;32m[TOTAL QUERIES: %s]\033[0m"
            % (" " * indentation, len(connection.queries))
        )
        return response

    return middleware
