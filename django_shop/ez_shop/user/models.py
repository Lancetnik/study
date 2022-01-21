from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from utils.models import FakeDeletionModel, FakeDeletionMixin


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{11}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed."
)


class UserAccountManager(FakeDeletionMixin, BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        if not password:
            raise ValueError('Password must be provided')

        if (email := extra_fields.get('email')) is not None:
            extra_fields['email'] = self.normalize_email(email)

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_confirmed'] = True
        return self._create_user(password, **extra_fields)


class NonDeletableUser(AbstractBaseUser, PermissionsMixin, FakeDeletionModel):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'login'

    objects = UserAccountManager()

    is_staff = models.BooleanField('staff status', default=False)
    is_confirmed = models.BooleanField('active', default=False)

    login = models.CharField(max_length=80, unique=True)
    email = models.EmailField('email', unique=True, blank=True, null=True)
    phone_number = models.CharField(
        validators=(phone_regex,), max_length=12,
        unique=True, blank=True, null=True
    )

    def get_short_name(self):
        return self.login

    def get_full_name(self):
        return f'{self.login}: {self.email}, {self.phone_number}'

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.get_short_name()

    def __repr__(self):
        return f'{self.id}: {self}'

    class Meta():
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
