import uuid
from datetime import date, datetime
from django.db import models

from business.utils import license_status

__all__ = [
    'Activity', 'License', 'Animal', 'User', 'Registry', 'AnimalRegistry'
]

# LICENCES MODELS
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
    activity = models.ForeignKey(
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


# SLAUGHTERHOUSE MODELS
class Animal(models.Model):
    name = models.CharField('Nombre', max_length=255)

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
    
    def __str__(self):
        return f'{ self.name }'


class AnimalRegistry(models.Model):
    registry = models.ForeignKey('Registry', on_delete=models.CASCADE)
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Cantidad')

    class Meta:
        verbose_name = 'Registro de animal'
        verbose_name_plural = 'Registro de animales'

    def __str__(self):
        return f'{ self.registry.user } { self.animal.name }'


class Registry(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'User', related_name='registries', on_delete=models.CASCADE
    )
    identification = models.ImageField('Identificación', blank=True, null=True) # TODO: remove blank and null
    animals = models.ManyToManyField(
        'Animal', through='AnimalRegistry'
    )

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self):
        return f'{ self.date } - { self.user.get_full_name() }'

    def get_formatted_date(self):
        return self.date.strftime('%d/%m/%Y, %H:%M')


class User(models.Model):
    first_name = models.CharField('Nombre', max_length=255)
    last_name = models.CharField('Apellido', max_length=255)
    curp = models.CharField('CURP', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f'{ self.get_full_name() }'

    def get_full_name(self):
        return f'{ self.first_name } { self.last_name }'