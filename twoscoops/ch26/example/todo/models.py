from django.conf import settings
from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='todos',
        on_delete=models.CASCADE
    )

