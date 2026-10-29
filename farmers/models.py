from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("agri_professional", "Agri-Professional"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Farm(models.Model):

    FARMING_CHOICES = [
        ("crop", "Crop Farming"),
        ("livestock", "Livestock Farming"),
        ("mixed", "Mixed Farming"),
        ("poultry", "Poultry Farming"),
        ("fish", "Fish Farming"),
        ("beekeeping", "Beekeeping"),
        ("other", "Other"),
    ]

    SOIL_CHOICES = [
        ("sandy", "Sandy"),
        ("clay", "Clay"),
        ("loam", "Loam"),
        ("silty", "Silty"),
        ("unknown", "Not Sure"),
    ]

    IRRIGATION_CHOICES = [
        ("rainfed", "Rain-fed"),
        ("drip", "Drip Irrigation"),
        ("sprinkler", "Sprinkler"),
        ("flood", "Flood Irrigation"),
        ("other", "Other"),
    ]

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="farms"
    )

    farm_name = models.CharField(max_length=150)

    farming_type = models.CharField(
        max_length=20,
        choices=FARMING_CHOICES
    )

    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places= 7,
        null= True,
        blank= True
    )
    longitude= models.DecimalField(
        max_digits= 10,
        decimal_places=7,
        null= True,
        blank=True
    )

    farm_size = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    size_unit = models.CharField(
        max_length=20,
        default="acres"
    )

    soil_type = models.CharField(
        max_length=20,
        choices=SOIL_CHOICES,
        default="unknown"
    )

    water_source = models.CharField(
        max_length=150,
        blank=True
    )

    irrigation_method = models.CharField(
        max_length=20,
        choices=IRRIGATION_CHOICES,
        blank=True
    )

    crops_planted = models.TextField(blank=True)
    other_crops = models.TextField(blank=True)

    livestock_types = models.TextField(blank=True)

    livestock_count = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    other_farming_details = models.TextField(blank=True)
    farming_challenges = models.TextField(blank=True)

    uses_fertilizer = models.BooleanField(default=False)
    fertilizer_details = models.TextField(blank=True)

    has_pests_or_diseases = models.BooleanField(default=False)
    pest_disease_details = models.TextField(blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farm_name} - {self.farmer.username}"

class ProfessionalProfile(models.Model):

    SPECIALIZATION_CHOICES = [
        ("crop_production", "Crop Production"),
        ("livestock", "Livestock Production"),
        ("poultry", "Poultry Farming"),
        ("dairy", "Dairy Farming"),
        ("horticulture", "Horticulture"),
        ("soil_science", "Soil Science"),
        ("irrigation", "Irrigation Management"),
        ("plant_health", "Plant Health and Disease Control"),
        ("animal_health", "Animal Health"),
        ("fisheries", "Fisheries"),
        ("beekeeping", "Beekeeping"),
        ("climate_smart", "Climate-Smart Agriculture"),
        ("agricultural_economics", "Agricultural Economics"),
        ("farm_mechanization", "Farm Mechanization"),
        ("other", "Other"),
    ]

    CONTACT_CHOICES = [
        ("phone", "Phone"),
        ("email", "Email"),
        ("in_app", "In-App Messaging"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professional_profile"
    )

    phone = models.CharField(max_length=20)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=120)
    qualification = models.CharField(max_length=150)
    specialization = models.CharField(
        max_length=40,
        choices=SPECIALIZATION_CHOICES
    )
    other_specialization = models.CharField(
        max_length=150,
        blank=True
    )
    experience_years = models.PositiveSmallIntegerField(default=0)

    services_offered = models.TextField(
        help_text="Describe the agricultural services you provide."
    )
    bio = models.TextField(
        blank=True,
        help_text="Describe your experience and how you help farmers."
    )

    working_days = models.CharField(max_length=150, blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    emergency_support = models.BooleanField(default=False)
    preferred_contact = models.CharField(
        max_length=10,
        choices=CONTACT_CHOICES,
        default="phone"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Professional Profile"
class SoilAssessment(models.Model):

    ASSESSMENT_TYPE_CHOICES = [
        ("laboratory", "Laboratory soil test"),
        ("field", "Field soil assessment"),
        ("other", "Other assessment"),
    ]

    REASON_CHOICES = [
        ("low-yield", "Investigating low crop yields"),
        ("fertility", "Checking soil fertility"),
        ("planting", "Preparing for planting"),
        ("nutrients", "Checking nutrient levels"),
        ("other", "Other reason"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending review"),
        ("reviewed", "Reviewed"),
    ]

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="soil_assessments"
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="soil_assessments"
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPE_CHOICES
    )

    assessment_date = models.DateField(
        null=True,
        blank=True
    )

    reason = models.CharField(
        max_length=20,
        choices=REASON_CHOICES
    )

    notes = models.TextField(blank=True)

    soil_file = models.FileField(
        upload_to="soil_assessments/%Y/%m/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm.farm_name} - Soil Assessment #{self.pk}"
class SoilRecommendation(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent to farmer"),
    ]

    assessment = models.ForeignKey(
        SoilAssessment,
        on_delete=models.CASCADE,
        related_name="recommendations"
    )

    professional = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="soil_recommendations"
    )

    findings = models.TextField(
        help_text="Professional's findings from the soil assessment."
    )

    recommendations = models.TextField(
        help_text="Recommended actions for the farmer."
    )

    fertilizer_advice = models.TextField(
        blank=True,
        help_text="Fertilizer or soil amendment advice, if applicable."
    )

    follow_up_advice = models.TextField(
        blank=True,
        help_text="Additional guidance and follow-up instructions."
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"Recommendation for Assessment "
            f"#{self.assessment_id}"
        )