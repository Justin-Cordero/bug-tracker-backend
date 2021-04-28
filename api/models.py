from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    github_username = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    developer = models.ManyToManyField(
        User, related_name='projects')


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ("None", "None"),
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    ]
    BUG_TYPE_CHOICES = [
        ("Bug/Error", "Bug/Error"),
        ("Typo", "Typo"),
        ("Feature Request", "Feature Request"),
        ("Other", "Other")
    ]
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
        ("In Work", "In Work"),
        ("Request More Info", "Request More Info")
    ]
    project = models.ForeignKey(
        Project, related_name='tickets', on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="None")
    type = models.CharField(
        max_length=20, choices=BUG_TYPE_CHOICES, default="Other")
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=18, choices=STATUS_CHOICES, default="Open")
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name='tickets', on_delete=models.CASCADE)


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
