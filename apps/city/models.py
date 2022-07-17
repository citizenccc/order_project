from django.db import models


class City(models.Model):
    city = models.CharField('City', max_length=255)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = 'Cities'