from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from uuid import UUID

from business.models import *
from business.serializers import *

from lib import response_status

# LICENCES API VIEWS
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
            raise Response({
                    'status': response_status.ERROR,
                    'error': 'No se encontró la licencia'
                }, status=status.HTTP_404_NOT_FOUND
            )
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'status': response_status.OK,
            'data': serializer.data
        }
        return Response(data)


# SLAUGHTERHOUSE API VIEWS
class AnimalList(generics.ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': response_status.OK,
            'data': serializer.data
        }
        return Response(data)


class RegistryList(generics.ListAPIView):
    serializer_class = RegistrySerializer

    def get_queryset(self):
        return Registry.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': response_status.OK,
            'data': serializer.data
        }
        return Response(data)


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': response_status.OK,
            'data': serializer.data
        }
        return Response(data)
    

class NewRegistry(APIView):

    def post(self, request, format=None):
        data = request.data
        user_instance = None
        new_registry = None
        response_data = None
        #  If the user has id get user, else create new user
        if 'id' in data['user'] and data['user']['id'] is not None:
            # Create new registry with existent user
            new_registry = Registry(user_id=data['user']['id'])
        else:
            user_serializer = UserSerializer(data=data['user'])
            if (user_serializer.is_valid()):
                user_instance = user_serializer.save()
                # Create new registry with new user
                new_registry = Registry(user=user_instance)
            else:
                response_data = {
                    'status': response_status.ERROR,
                    'error': user_serializer.errors,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        new_registry.save()
        animals_registry = [
            AnimalRegistry(animal_id=animal['id'], registry=new_registry, quantity=animal['quantity']) for animal in data['animals']
        ]

        AnimalRegistry.objects.bulk_create(animals_registry)

        registry_serializer = RegistrySerializer(instance=new_registry)
        
        response_data = {
            'status': response_status.OK,
            'data': registry_serializer.data,
        }

        return Response(response_data)
    
