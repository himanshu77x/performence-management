from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Extend User model to include Role & Reporting Manager
class Profile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('TL', 'TL'),
        ('Employee', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    reporting_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reportees')

    def __str__(self):
        return self.user.username

# Review Model
class Review(models.Model):
    PERIOD_CHOICES = (
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    )
    title = models.CharField(max_length=255)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review_date = models.DateField()
    review_period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.employee.username}"
