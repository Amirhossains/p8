import random

from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, send_mail, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _craete_user(self, username, email, password, phone_number, is_staff, is_superuser, **extra_fields):
        """
        Craetes and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          password=password,
                          phone_number=phone_number,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields
                          )
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz')+str(phone_number)[-7:]
            while User.objects.filter(username=username).exist():
                username += str(random.randint(10, 99))

        return self._craete_user(username=username, phone_number=phone_number, password=password, email=email, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, username, phone_number, password, email, **extra_fields):
        return self._craete_user(username=username, email=email, password=password, phone_number=phone_number, is_staff=True, is_superuser=True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number':phone_number})

class User(PermissionsMixin, AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(verbose_name='username', max_length=32 ,unique=True,
                                help_text='Required! 30 character of fewer starting with a letter.',
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',(
                                                              'Enter a valid username starting with a-z.'
                                                              'This value may contain only letters, numbers'
                                                              ', symbols and underscore charecters.'), 'invalid')
                                ],
                                error_messages = {
                                    'unique':'A user with that username is already exists.'
                                }
                                )
    first_name = models.CharField(verbose_name='first name', blank=True, max_length=30)
    last_name = models.CharField(verbose_name='last name', blank=True, max_length=30)
    email = models.CharField(verbose_name='email address', max_length=50, blank=True, null=True, unique=True)
    phone_number = models.PositiveBigIntegerField(verbose_name='phone number', blank=True, null=True, unique=True,
                                               validators=[
                                                   validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                             ('Enter a valid number'),
                                                                             'invalid')

                                               ],
                                               error_messages={
                                                   'unique' : 'A phone number with that number is already exists.'
                                               }
                                               )
    is_staff = models.BooleanField(verbose_name='is staff', default=False,
                                   help_text='Designates wheter the user can log into this admin site.')
    is_active = models.BooleanField(verbose_name='is superuser', default=True,
                                       help_text='Designates wheter this user should be treated as active.'
                                                 'Unselect this instead of deleting account.')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_seen = models.DateTimeField(verbose_name='last seen date', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the users.
        """
        return self.first_name

    def email_user(self, subject, message, form_email=None, **kwargs):
        """
        send an email for this user.
        """
        send_mail(subject, message, form_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        """
        Returns True if user has actully logged in with valid credentials.
        """
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

class Province(models.Model):
    name = models.CharField(max_length=20)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    craeted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    User     = models.OneToOneField(to=User, on_delete=models.CASCADE)
    NickName = models.CharField(verbose_name='nick name', max_length=30, blank=True)
    Avatar   = models.ImageField(verbose_name='avatar', blank=True, null=True)
    Birthday = models.PositiveIntegerField(verbose_name='birthday', blank=True, null=True)
    man      = 1
    woman    = 2
    gender   = ((man, 'man'), (woman, 'woman'))
    Generic  = models.IntegerField(verbose_name='gender', choices=gender, default=man)
    Province = models.ForeignKey(verbose_name='province', null=True, to=Province, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user_profile'
        verbose_name_plural = 'user_profiles'

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android')
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='devices')
    device_uuid = models.UUIDField(verbose_name='Device', null=True)
    last_login = models.DateTimeField(verbose_name='last login date', null=True)
    device_type = models.PositiveSmallIntegerField(verbose_name='device model', choices=DEVICE_TYPE_CHOICES, default=ANDROID)
    device_os = models.CharField(verbose_name='device os', max_length=20, blank=True)
    device_model = models.CharField(verbose_name='device model', max_length=50, blank=True)
    app_version = models.CharField(verbose_name='app version', max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        unique_together = ('user', 'device_uuid')


