from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from django.shortcuts import get_object_or_404
from django.http import Http404
from uuid import UUID

from business.models import *
from business.serializers import *

from lib import response_status


class LicenseDetail(generics.RetrieveAPIView):
    serializer_class = LicenseSerializer

    def get_queryset(self):
        return License.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            uuid_code = UUID(self.kwargs['uuid_code'], version=4)
            obj = get_object_or_404(queryset ,uuid_code=uuid_code)
        except ValueError as e:
            raise Http404("No se encontró la licencia")
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'status': response_status.OK,
            'data': serializer.data
        }
        return Response(data)
    
