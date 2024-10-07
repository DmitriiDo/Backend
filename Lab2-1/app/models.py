from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Vehicle(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="images/default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    price = models.IntegerField(blank=True, null=True)
    category = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комплектующие"
        verbose_name_plural = "Комплектующии"
        db_table = "vehicles"


class Production(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    weight = models.IntegerField(verbose_name="Фактическая масса", blank=True, null=True)

    def __str__(self):
        return "Заявка №" + str(self.pk)

    def get_vehicles(self):
        return [
            setattr(item.vehicle, "value", item.value) or item.vehicle
            for item in VehicleProduction.objects.filter(production=self)
        ]

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ('-date_formation', )
        db_table = "productions"


class VehicleProduction(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, blank=True, null=True)
    production = models.ForeignKey(Production, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "vehicle_production"
