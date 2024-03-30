from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.db import models

# Create your models here.

from django.db import models
from .choices import OrgnizationTypeChoices

from django.db import models


class Employee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    joining_date = models.DateField()
    orgn = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15)
    emergency_mobile = models.CharField(max_length=15)
    birth_date = models.DateField()
    marriage_date = models.DateField()
    address = models.TextField()
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    orgn = models.CharField(max_length=3, choices=OrgnizationTypeChoices, validators=[OrgnizationTypeChoices.validator])

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'book'
        db_table = 'Employee Master'


class User(AbstractUser):
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, default=0, db_index=True)
    username = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')

    objects = UserManager()

    def __str__(self):
        return self.username


class Book(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=30, default='anonymous')
    email = models.EmailField(blank=True)
    describe = models.TextField(default='DataFlair Django tutorials')

    def __str__(self):
        return self.name


class SuperAdminUser(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    department = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=7)
    zone = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class SuperAdminUserActivity(models.Model):
    mobile = models.ForeignKey(SuperAdminUser, on_delete=models.CASCADE)
    # mobile = models.CharField(max_length=20)
    url_endpoint = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.mobile
