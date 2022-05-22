from django.contrib.auth import get_user_model
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    tax_number = models.CharField('ИНН', max_length=10, unique=True, db_index=True)
    base_tax_number = models.CharField('ОГРН', max_length=13, unique=True, db_index=True)
    legal_address = models.CharField('Юр. адрес', max_length=255, default='')
    site_url = models.URLField()


class Company(models.Model):
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    tax_number = models.CharField('ИНН', max_length=10, unique=True, db_index=True)
    legal_address = models.CharField('Юр. адрес', max_length=255, default='', blank=True)
    verification_date = models.DateField(blank=True, null=True)
    info = models.TextField(default='')
    info_url = models.URLField()
    users = models.ManyToManyField(get_user_model(), related_name='companies', blank=True)
