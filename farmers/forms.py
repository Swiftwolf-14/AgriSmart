from django import forms
from .models import Farm
from .models import ProfessionalProfile, SoilRecommendation



class FarmForm(forms.ModelForm):

    class Meta:
        model = Farm

        fields = [
            "farm_name",
            "farming_type",
            "county",
            "sub_county",
            "village",
            "latitude",
            "longitude",
            "farm_size",
            "size_unit",
            "soil_type",
            "water_source",
            "irrigation_method",
            "crops_planted",
            "other_crops",
            "livestock_types",
            "livestock_count",
            "other_farming_details",
            "farming_challenges",
            "uses_fertilizer",
            "fertilizer_details",
            "has_pests_or_diseases",
            "pest_disease_details",
            "notes",
        ]

        widgets = {
            "crops_planted": forms.Textarea(
                attrs={"rows": 3}
            ),
            "other_crops": forms.Textarea(
                attrs={"rows": 2}
            ),
            "livestock_types": forms.Textarea(
                attrs={"rows": 2}
            ),
            "other_farming_details": forms.Textarea(
                attrs={"rows": 3}
            ),
            "farming_challenges": forms.Textarea(
                attrs={"rows": 3}
            ),
            "fertilizer_details": forms.Textarea(
                attrs={"rows": 2}
            ),
            "pest_disease_details": forms.Textarea(
                attrs={"rows": 2}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3}
            ),
        }


class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = [
            "phone",
            "county",
            "sub_county",
            "organization",
            "job_title",
            "qualification",
            "specialization",
            "other_specialization",
            "experience_years",
            "services_offered",
            "bio",
            "working_days",
            "working_hours",
            "emergency_support",
            "preferred_contact",
        ]

        widgets = {
            "services_offered": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "E.g. crop management, soil advice, farm visits..."
            }),
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Introduce yourself and describe your experience."
            }),
            "working_days": forms.TextInput(attrs={
                "placeholder": "E.g. Monday to Friday"
            }),
            "working_hours": forms.TextInput(attrs={
                "placeholder": "E.g. 8:00 AM - 5:00 PM"
            }),
        }

class SoilRecommendationForm(forms.ModelForm):

    class Meta:
        model = SoilRecommendation

        fields = [
            "findings",
            "recommendations",
            "fertilizer_advice",
            "follow_up_advice",
        ]

        widgets = {
            "findings": forms.Textarea(
                attrs={"rows": 4}
            ),
            "recommendations": forms.Textarea(
                attrs={"rows": 5}
            ),
            "fertilizer_advice": forms.Textarea(
                attrs={"rows": 3}
            ),
            "follow_up_advice": forms.Textarea(
                attrs={"rows": 3}
            ),
        }