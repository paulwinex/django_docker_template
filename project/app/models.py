from django.db import models


class Dummy(models.Model):
    value = models.CharField('Value', max_length=128, blank=True, default='')
