from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches')
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search by {self.user.username} at {self.created_at}: {self.query}"


class RegistrationCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Code {self.code} - {'Used' if self.is_used else 'Available'}"

    def is_valid(self):
        """Check if the code is still valid (not used and not expired)"""
        return not self.is_used and self.expires_at > timezone.now()

    def use_code(self, user):
        """Mark the code as used by a specific user"""
        self.is_used = True
        self.used_by = user
        self.used_at = timezone.now()
        self.save()

    @classmethod
    def create_code(cls, code, days_valid=30):
        """Create a new registration code valid for specified days"""
        expires_at = timezone.now() + timedelta(days=days_valid)
        return cls.objects.create(code=code, expires_at=expires_at)
