# employee/models.py
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, Permission, Group)
from django.db import models

class EmployeeManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    # Связи с группами и правами
    groups = models.ManyToManyField(
        Group,
        related_name='employee_set',  # Указываем уникальное имя для связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',
        # Указываем уникальное имя для связи
        blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    def __str__(self):
        return self.username

class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.position}"



