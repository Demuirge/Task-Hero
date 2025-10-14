from django.db import models

from django.contrib.auth import get_user_model

from django.core.validators import MinLengthValidator

User = get_user_model()

# Create your models here.

class PriorityChoices(models.TextChoices):
    LOW = 'L', 'Low'
    MEDIUM = 'M', 'Medium'
    HIGH = 'H', 'High'

class StatusChoices(models.TextChoices):
    TO_DO = 'TD', 'To Do'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'C', 'Completed'

class Task(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    description = models.TextField(validators=[MinLengthValidator(10)])
    due_date = models.DateField()
    status = models.CharField(max_length=2, choices=StatusChoices.choices)
    priority = models.CharField(max_length=2, choices=PriorityChoices.choices)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.creator}"