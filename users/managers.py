from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from neo3 import wallet


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where wallet addresss is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, wallet_address, password, **extra_fields):
        """
        Create and save a User with the given wallet_address and password.
        """
        if not wallet_address:
            raise ValueError(_('The Wallet adresss must be set'))
        wallet.Account.validate_address(wallet_address)
        beginning_slice = slice(5)
        beginning_text = wallet_address[beginning_slice]
        ending_slice = slice(31,34,1)
        ending_text = wallet_address[ending_slice]
        sliced_address = beginning_text + ending_text
        user = self.model(wallet_address=wallet_address, **extra_fields)
        user.set_password(sliced_address)
        user.save()
        return user

    def create_superuser(self, wallet_address, password, **extra_fields):
        """
        Create and save a SuperUser with the given wallet_address and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(wallet_address, password, **extra_fields)