from django.urls import path

from business.views.api import *

app_name = 'BusinessApi'


urlpatterns = [
    # Tenant
    # path('tiendas/', TenantList.as_view(),name='tenants'),
    path('licencias/<uuid_code>/', LicenseDetail.as_view(), name='license'),
]