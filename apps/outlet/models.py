from django.db import models

from apps.city.models import City


class Outlet(models.Model):
    city = models.ForeignKey(City, related_name='outlet_city', on_delete=models.CASCADE, verbose_name='City')
    title = models.CharField('Title', max_length=255)
    logo = models.ImageField('Outlet logo', upload_to='outlet_logos', blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
    img = models.ImageField('Photo', upload_to='outlet_images', null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Outlet'
        verbose_name_plural = 'Outlet'


class OutletImage(models.Model):
    outlet = models.ForeignKey(Outlet, related_name='outlet_images', on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='outlet_images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Photo outlet'