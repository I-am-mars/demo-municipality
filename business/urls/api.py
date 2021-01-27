from django.urls import path

from business.views.api import *

app_name = 'BusinessApi'


urlpatterns = [
    # Licencias
    path('licencias/<uuid_code>/', LicenseDetail.as_view(), name='license'),
    # Rastro municipal
    path('rastro-municipal/usuarios/', UserList.as_view(), name='users'),
    path('rastro-municipal/nuevo-registro/', NewRegistry.as_view(), name='new_registry'),
    path('rastro-municipal/registros/', RegistryList.as_view(), name='registries'),
    path('rastro-municipal/animales/', AnimalList.as_view(), name='animals'),
]