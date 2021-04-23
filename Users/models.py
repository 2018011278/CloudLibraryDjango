from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('male', "男"),
        ('female', "女"),
        ('secret', "保密")
    )
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default='secret')
    stu_id = models.BigIntegerField(null=True, blank=True)
    department = models.CharField(max_length=254, default='电脑系')
    remarks = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return '/users/%i/' % self.pk

    def email_verified(self):
        if self.is_authenticated:
            result = EmailAddress.objects.filter(email=self.email)
            if len(result):
                return result[0].verified
        else:
            return False


class Info(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    floor = models.CharField(max_length=10)
    detail = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return '/info/%i' % self.pk
