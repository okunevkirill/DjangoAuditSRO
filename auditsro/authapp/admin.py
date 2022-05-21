from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('pk', 'email', 'is_superuser', 'is_active', 'phone', 'updated_at')
    list_display_links = ('pk', 'email')
    list_filter = ('is_superuser', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': (('email', 'phone'), ('first_name', 'last_name'), 'created_at', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (('email', 'phone'), 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    search_fields = ('email', 'pk')
    ordering = ('email',)

# admin.site.register(CustomUser, CustomUserAdmin)
