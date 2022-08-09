from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    wallet_address = models.CharField(_('wallet address'), unique=True, max_length=34)
    email = models.EmailField(_('email address'), blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'wallet_address'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.wallet_address

    def shortened_address(self):
        beginning_slice = slice(5)
        beginning_text = self.wallet_address[beginning_slice]
        ending_slice = slice(31,34,1)
        ending_text = self.wallet_address[ending_slice]
        return f"{beginning_text}...{ending_text}"