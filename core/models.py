from django.db import models
from django.contrib.auth.models import User


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    discipline = models.CharField(max_length=100)
    skill_level = models.IntegerField()
    experience_years = models.IntegerField()
    injury_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Athlete', 'Athlete'),
        ('Coach', 'Coach'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gym = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class TrainingSession(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    discipline = models.CharField(max_length=100, default="Boxing")
    duration = models.IntegerField()
    intensity = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.athlete.user.username


class InjuryReport(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    injury_type = models.CharField(max_length=100)
    severity = models.IntegerField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.athlete.user.username


class Availability(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.athlete.user.username