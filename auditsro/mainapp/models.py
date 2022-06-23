from django.contrib.auth import get_user_model
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    tax_number = models.CharField('ИНН', max_length=12, unique=True, db_index=True)
    base_tax_number = models.CharField('ОГРН', max_length=15, unique=True, db_index=True)
    legal_address = models.CharField('Юр. адрес', max_length=255, default='')
    site_url = models.URLField()

    def __str__(self):
        return f'Organization(pk={self.pk}, naime={self.name})'


class Company(models.Model):
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    tax_number = models.CharField('ИНН', max_length=12, unique=True, db_index=True)
    legal_address = models.CharField('Юр. адрес', max_length=255, default='', blank=True)
    verification_date = models.DateField(blank=True, null=True)
    info = models.TextField(default='')
    info_url = models.URLField()

    def __str__(self):
        return f'Company(pk={self.pk}, naime={self.name})'


class TrackedList(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company, blank=True)
