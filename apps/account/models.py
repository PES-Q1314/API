from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UPCUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_active=True, last_login=now, date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UPCUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, unique=True)
    email = models.EmailField('email address', blank=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_active = models.BooleanField(default=True)

    objects = UPCUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
