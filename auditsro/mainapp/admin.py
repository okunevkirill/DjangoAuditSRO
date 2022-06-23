from django.contrib import admin

from .models import Company, Organization, Watchlist


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active', 'tax_number', 'info_url')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'tax_number')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active', 'tax_number', 'site_url')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'tax_number')


@admin.register(Watchlist)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    list_display_links = ('pk', 'user')
    search_fields = ('user',)
