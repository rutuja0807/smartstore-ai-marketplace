from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)

    # These two blocks solve the "Reverse Accessor Clash" error
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', 
        blank=True,
    )

    def __str__(self):
        return self.username