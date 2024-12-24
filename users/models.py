from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        # Separate many-to-many fields if any
        groups = other_fields.pop("groups", None)  # Assuming "groups" is a many-to-many field
        user_permissions = other_fields.pop("user_permissions",
                                            None)  # Similarly for user_permissions if applicable
        other_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    subdomain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=6, null=True, blank=True)
    notification_token = models.CharField(max_length=255, null=True, blank=True)
    objects = CustomAccountManager()
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    uer_hash_code = models.CharField(max_length=255, null=True, blank=True)
    is_social = models.BooleanField(default=False)
    platform = models.CharField(max_length=255, null=True, blank=True)
    reset_expire_time = models.DateTimeField(null=True, blank=True)
    secret_key = models.CharField(max_length=255, null=True, blank=True)
    encrypted_user_id = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=255, null=True, blank=True)
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        """
        Automatically set username to `first_name + ' ' + last_name` if not provided.
        """
        if not self.username:
            self.username = self.get_full_name()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "aauth_users"
