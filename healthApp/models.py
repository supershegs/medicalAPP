from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid

# Create your models here.
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
        
        
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.name = uuid.uuid4()
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)  
    phone_no = models.CharField(max_length=21)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=21)
    emergency_contact_name = models.CharField(max_length=250)
    emergency_contact_no = models.CharField(max_length=21)
    avatar = models.ImageField(upload_to='profile_pic/', null=True,
        blank=True,
        default='profile_pic/default_avatar.png')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title
    
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title

class Consultant(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    area_of_specialization = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='consultant_pic/')

    def __str__(self):
        return self.name

class HealthInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health_condition = models.TextField()
    drugs_prescribed = models.TextField()
    complaints = models.TextField()
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    call_consultant = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    body_weight = models.DecimalField(max_digits=5, decimal_places=2)
    heart_rate = models.PositiveIntegerField()
    existing_conditions = models.TextField()
    blood_group = models.CharField(max_length=5)
    blood_pressure = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='medical_record_pic/', null=True,
        blank=True)
    

    def __str__(self):
        return f"Health Information for {self.user.name}"