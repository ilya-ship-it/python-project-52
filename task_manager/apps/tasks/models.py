from django.db import models

from ..labels.models import Label

# Create your models here.


class Task(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        related_name='statuses'
        )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='authors'
        )
    executor = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='executors',
        blank=True
        )
    labels = models.ManyToManyField(
        Label,
        through='tasks_labels',
        through_fields=('task', 'label'),
        blank=True
        )
    created_at = models.DateTimeField(auto_now_add=True)


class tasks_labels(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        related_name='tasks',
        null=True
        )
    label = models.ForeignKey(
        Label,
        on_delete=models.PROTECT,
        related_name='labels'
    )
