import uuid
from datetime import date, datetime
from django.db import models

from business.utils import license_status 

__all__ = [
    'Activity', 'License'
]


class Activity(models.Model):
    name = models.CharField('Nombre', max_length=255)


    class Meta:
        verbose_name = 'Actividad comercial'
        verbose_name_plural = 'Actividades comerciales'

    def __str__(self):
        return f'{ self.name }'


class License(models.Model):
    uuid_code = models.UUIDField(default=uuid.uuid4, editable=False)
    folio = models.CharField('Folio', max_length=255, unique=True)
    activity = models.OneToOneField(
        'Activity', related_name='license', on_delete=models.DO_NOTHING
    )
    valid_until = models.DateField('Fecha de vencimiento')


    class Meta:
        verbose_name = 'Licencia'
        verbose_name_plural = 'Licencias'

    def __str__(self):
        return f'{ self.uuid_code } - { self.folio }'
    
    def get_status(self):
        expired = date.today() > self.valid_until
        if expired:
            return license_status.EXPIRED
        return license_status.ACTIVE

    def get_expired_time(self):
        if self.get_status() == license_status.EXPIRED:
            expired_days = (date.today() - self.valid_until).days
            return f'{expired_days} { "día" if expired_days == 1 else "días" }'
        return None