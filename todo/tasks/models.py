from taggit.managers import TaggableManager

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=250, db_index=True)
    is_completed = models.BooleanField(verbose_name=_("Is completed?"), default=False)
    user = models.ForeignKey(
        verbose_name=_("User"), to=settings.AUTH_USER_MODEL, related_name="tasks", on_delete=models.CASCADE
    )
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return f"{self.title}"
