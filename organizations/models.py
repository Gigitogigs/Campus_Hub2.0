from django.db import models
import uuid
from accounts.models import UserPublic

# Create your models here.

class University(models.Model):
    """ 
        Represents a university on the platform.
        Scaffold for multi-tenancy. Only KU in MVP, but FK is in place for future expansion.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    email_domain = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'universities'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

    
    
class Organization(models.Model):
    """
    Represents a student club, society, or administrative body.
    Scoped to a university - name uniqueness is per university. Not global
    """
    ORG_CLASS = [('student', 'Student'), ('administrative', 'Administrative')]
    ORG_TYPE = [('club', 'Club'), ('society', 'Society'), ('department', 'Department'), ('office', 'Office'), ('group', 'Group')]
    CATEGORIES = [
        ('academic', 'Academic'),
        ('tech', 'Tech'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('business', 'Business'),
        ('religous', 'Religious'),
        ('other', 'Other')
    ]    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='organizations')
    name = models.CharField(max_length=255)
    description = models.TextField()
    organization_type = models.CharField(max_length=20, choices=ORG_TYPE)
    organization_class = models.CharField(max_length=20, choices=ORG_CLASS)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='organization_covers/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['university', 'name'],
                name='unique_organization_name_per_university'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.university.short_name})"

class OrganizationMember(models.Model):
    """
    Model representing a member of an organization.
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'
        
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserPublic, on_delete=models.CASCADE, related_name='organization_memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    is_creator = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organization_members'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'user'],
                name='unique_organization_membership'
            ),
            models.CheckConstraint(
                condition=models.Q(role__in=['admin', 'member']),
                name='Valid_role_check'
            ),
            models.CheckConstraint(
                condition=~models.Q(is_creator=True) | models.Q(role='admin'),
                name='creator_must_be_admin'
            )
        ]

    def __str__(self):
        return f"{self.user.display_name} in {self.organization.name} ({self.role})"

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserPublic, on_delete=models.CASCADE, related_name="following")
    Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'follows'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'user'],
                name='unique_organization_follower'
            )
        ]
    
    def __str__(self):
        return f"{self.user.display_name} follows {self.organization.name}"