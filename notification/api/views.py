from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from .serializers import NotifSerializer

from rest_framework.response import Response
from rest_framework import status

from notification.models import Notifikasi


class UserNotifikasiApiView(ListModelMixin, GenericAPIView):
    serializer_class = NotifSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Notifikasi.objects.filter(receiver=self.request.user, is_seen=False)
        # kalau notif terlalu dikit tambah 10 notif lalu
        if len(qs) <= 10:
            queryTambahan = Notifikasi.objects.filter(
                receiver=self.request.user,
                is_seen=True,
            )[:20]
            qs = qs | queryTambahan
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.user = self.get_object()
        idUpdate =dict(request.data).get('id',False) 
        if self.user.is_authenticated:
            if idUpdate:
                query = Notifikasi.objects.filter(id=idUpdate)
                query.update(is_seen=False)
            else:
                query = Notifikasi.objects.filter(receiver=self.user, is_seen=False)
                query.update(is_seen=True)
          
            return Response(status=status.HTTP_200_OK)

        return Response(
            {"user": ["user not authorized or not your"]},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def get_object(self, queryset=None):
        return self.request.user
