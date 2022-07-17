from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models

from main.settings import ALLOWED_HOSTS, EMAIL_HOST_USER, HOST


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class ContactChoices(models.TextChoices):
    whatsapp = ('whatsapp', 'WhatsApp')
    telephone = ('telephone', 'Телефон')
    mail = ('mail', 'Мейл')


class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)
    name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    contact_method = models.CharField(max_length=50, blank=True, choices=ContactChoices.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(6, '0123456789')
        self.activation_code = code
        self.save()

    def activate_with_code(self, activation_code):
        if self.activation_code != activation_code:
            raise Exception('Неверный код активации')
        self.is_active = True
        self.activation_code = ''
        self.save()

    def send_activation_email(self):
        message = f"""
        Благодарим Вас за регистрацию на нашем сайте.
        Ваш код активации:  https://{HOST}/api/v1/auth/activate/{self.activation_code}/
        """
        send_mail('Активация аккаунта',
                  message,
                  EMAIL_HOST_USER,
                  [self.email],
                  )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'


