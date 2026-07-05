from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# Create your managers here.
class UserManager(BaseUserManager):
    """
    Custom user manager where university_email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, university_email, password=None, **extra_fields):
        if not university_email:
            raise ValueError("The University Email field must be set")
        university_email = self.normalize_email(university_email)
        user = self.model(university_email=university_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, university_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(university_email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model. Stores PII + auth credentials
    Table users_pii
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university_email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'university_email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users_pii'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.university_email
    
    
class UserPublic(models.Model):
    """
        Public use model. Store user information that is safe to share with the public.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey('organizations.University', on_delete=models.SET_NULL, null=True, related_name='public_profiles')
    anonymous_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='public_profile')
    display_name = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    course = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_public'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_public_profile')
        ]
    
    def __str__(self):
        return self.display_name
    