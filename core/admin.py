from django.contrib import admin
from .models import Athlete, TrainingSession, InjuryReport, UserProfile, Availability

admin.site.register(Athlete)
admin.site.register(TrainingSession)
admin.site.register(InjuryReport)
admin.site.register(UserProfile)
admin.site.register(Availability)