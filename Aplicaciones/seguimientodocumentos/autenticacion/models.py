import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


def default_expiry():
    return timezone.now() + timedelta(days=1)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Usamos la función `default_expiry` en lugar de lambda
    expires_at = models.DateTimeField(default=default_expiry)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Token para {self.user}"