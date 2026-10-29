from django.contrib import admin
from .models import UserProfile, SoilAssessment,SoilRecommendation

admin.site.register(UserProfile)
admin.site.register(SoilAssessment)
admin.site.register(SoilRecommendation)
