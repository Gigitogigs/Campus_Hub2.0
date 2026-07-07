from django.db import models
from organizations.models import Organization
from accounts.models import UserPublic
import uuid

# Create your models here.
class BasePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='%(class)s_posts', null=True, blank=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(UserPublic, on_delete=models.CASCADE, related_name='%(class)s_posts', null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Event(BasePost):
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=255)

    class Meta:
        db_table = 'events'

class Post(BasePost):
    class Meta:
        db_table = 'posts'
