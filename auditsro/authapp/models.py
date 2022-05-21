from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from authapp.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    phone = models.CharField('phone number', max_length=11, blank=True)
    first_name = models.CharField(_("first name"), max_length=64, blank=True)
    last_name = models.CharField(_("last name"), max_length=64, blank=True)
    created_at = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField("date update", default=timezone.now)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'User(pk={self.pk}, email={self.email})'
