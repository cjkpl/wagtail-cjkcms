from django.conf import settings
from django.db import models


class AdminListingPreference(models.Model):
    """Personal display options, independent of project user/profile models."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    listing_key = models.CharField(max_length=255)
    hidden_columns = models.JSONField(default=list, blank=True)
    page_size = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "listing_key"], name="cjkcms_unique_listing_preference"
            )
        ]
