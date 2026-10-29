from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    FarmForm,
    ProfessionalProfileForm,
    SoilRecommendationForm,
)

from .models import (
    Farm,
    ProfessionalProfile,
    SoilAssessment,
    SoilRecommendation,
    UserProfile,
)


def register_view(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(
            user=request.user
        ).first()

        if profile:
            if profile.role == "farmer":
                return redirect("farmer_dashboard")

            if profile.role == "agri_professional":
                return redirect("agri_professional_dashboard")

    if request.method == "POST":
        full_name = request.POST.get(
            "full_name", ""
        ).strip()

        username = request.POST.get(
            "username", ""
        ).strip()

        email = request.POST.get(
            "email", ""
        ).strip()

        password = request.POST.get("password", "")

        confirm_password = (
            request.POST.get("confirm_password")
            or request.POST.get("confirm_Password", "")
        )

        role = request.POST.get(
            "role", ""
        ).strip().lower()

        if not all([
            full_name,
            username,
            email,
            password,
            confirm_password,
        ]):
            messages.error(
                request,
                "Please fill in all required fields."
            )

        elif role not in (
            "farmer",
            "agri_professional",
        ):
            messages.error(
                request,
                "Please select a valid account type."
            )

        elif password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )

        elif len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

        elif User.objects.filter(
            username__iexact=username
        ).exists():
            messages.error(
                request,
                "Username already exists. Please choose another."
            )

        elif User.objects.filter(
            email__iexact=email
        ).exists():
            messages.error(
                request,
                "Email is already registered. Please log in."
            )

        else:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name,
                    )

                    UserProfile.objects.create(
                        user=user,
                        role=role,
                    )

                login(request, user)

                if role == "farmer":
                    return redirect("farmer_dashboard")

                return redirect("agri_professional_dashboard")

            except IntegrityError:
                messages.error(
                    request,
                    "Registration failed. Please try another "
                    "username or email."
                )

    return render(
        request,
        "register/register.html",
    )


def login_view(request):
    if request.method == "GET":
        storage = messages.get_messages(request)
        list(storage)

    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(
            user=request.user
        ).first()

        if profile:
            if profile.role == "farmer":
                return redirect("farmer_dashboard")

            if profile.role == "agri_professional":
                return redirect("agri_professional_dashboard")

    if request.method == "POST":
        identifier = request.POST.get(
            "username_or_email", ""
        ).strip()

        password = request.POST.get("password", "")

        if not identifier or not password:
            messages.error(
                request,
                "Please enter your username or email and password."
            )

        else:
            user_account = User.objects.filter(
                username__iexact=identifier
            ).first()

            if user_account is None:
                user_account = User.objects.filter(
                    email__iexact=identifier
                ).first()

            if user_account is None:
                messages.error(
                    request,
                    "Account not found. Please register first."
                )

            else:
                user = authenticate(
                    request,
                    username=user_account.username,
                    password=password,
                )

                if user is None:
                    messages.error(
                        request,
                        "Incorrect password. Please try again."
                    )

                else:
                    profile = UserProfile.objects.filter(
                        user=user
                    ).first()

                    if profile is None:
                        messages.error(
                            request,
                            "Your account role is not configured. "
                            "Please contact support."
                        )

                    elif profile.role == "farmer":
                        login(request, user)

                        return redirect("farmer_dashboard")

                    elif profile.role == "agri_professional":
                        login(request, user)

                        return redirect(
                            "agri_professional_dashboard"
                        )

                    else:
                        messages.error(
                            request,
                            "Invalid account role. Please contact support."
                        )

    return render(
        request,
        "login/login.html",
    )



@login_required(login_url="login")
def farmer_dashboard_view(request):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        messages.error(
            request,
            "Your account role is not configured."
        )

        return redirect("login")

    if profile.role != "farmer":
        if profile.role == "agri_professional":
            return redirect("agri_professional_dashboard")

        messages.error(
            request,
            "Invalid account role."
        )

        return redirect("login")

    farms = Farm.objects.filter(
        farmer=request.user
    ).order_by("-created_at")

    selected_farm = None
    farm_id = request.GET.get("farm")

    if farm_id:
        selected_farm = farms.filter(
            id=farm_id
        ).first()

    if selected_farm is None:
        selected_farm = farms.first()

    return render(
        request,
        "dashboard/farmer_dashboard.html",
        {
            "profile": profile,
            "farms": farms,
            "selected_farm": selected_farm,
        },
    )




@login_required(login_url="login")
def agri_professional_dashboard_view(request):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        messages.error(
            request,
            "Your account role is not configured."
        )

        return redirect("login")

    if profile.role != "agri_professional":
        if profile.role == "farmer":
            return redirect("farmer_dashboard")

        messages.error(
            request,
            "Invalid account role."
        )

        return redirect("login")

    return render(
        request,
        "dashboard/agri_professional_dashboard.html",
        {
            "profile": profile,
        },
    )



def logout_view(request):
    if request.method == "POST":
        logout(request)

        messages.success(
            request,
            "You have been logged out successfully. Login again."
        )

    return redirect("login")




@login_required(login_url="login")
def add_farm_view(request):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "farmer":
        messages.error(
            request,
            "Only farmers can register a farm."
        )

        return redirect("home")

    if request.method == "POST":
        form = FarmForm(request.POST)

        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = request.user
            farm.save()

            messages.success(
                request,
                "Farm details saved successfully!"
            )

            return redirect("my_farms")

    else:
        form = FarmForm()

    return render(
        request,
        "dashboard/add_farm.html",
        {
            "form": form,
        },
    )


# ============================================================
# MY FARMS
# ============================================================

@login_required(login_url="login")
def my_farms_view(request):
    farms = Farm.objects.filter(
        farmer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/my_farms.html",
        {
            "farms": farms,
        },
    )



@login_required(login_url="login")
def professional_farmers_view(request):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "agri_professional":
        messages.error(
            request,
            "You are not authorized to view this page."
        )

        return redirect("home")

    farmers = User.objects.filter(
        profile__role="farmer"
    ).select_related(
        "profile"
    ).order_by("username")

    search_query = request.GET.get(
        "search", ""
    ).strip()

    if search_query:
        farmers = farmers.filter(
            Q(username__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(farms__county__icontains=search_query)
        ).distinct()

    return render(
        request,
        "dashboard/professional_farmers.html",
        {
            "farmers": farmers,
            "search_query": search_query,
        },
    )




@login_required(login_url="login")
def professional_farmer_detail_view(request, farmer_id):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "agri_professional":
        messages.error(
            request,
            "You are not authorized to view this page."
        )

        return redirect("home")

    farmer = get_object_or_404(
        User.objects.select_related("profile"),
        pk=farmer_id,
        profile__role="farmer",
    )

    farms = Farm.objects.filter(
        farmer=farmer
    ).order_by("-created_at")

    assessments = SoilAssessment.objects.filter(
        farmer=farmer
    ).select_related(
        "farm"
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/professional_farmer_detail.html",
        {
            "farmer": farmer,
            "farms": farms,
            "assessments": assessments,
        },
    )


@login_required(login_url="login")
def professional_profile_view(request):
    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if (
        not user_profile
        or user_profile.role != "agri_professional"
    ):
        messages.error(
            request,
            "Only agricultural professionals can access this page."
        )

        return redirect("login")

    profile, created = ProfessionalProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfessionalProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your professional profile has been saved successfully."
            )

            return redirect("professional_profile")

    else:
        form = ProfessionalProfileForm(
            instance=profile
        )

    return render(
        request,
        "dashboard/professional_profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )


# ============================================================
# SESSION TIMEOUT
# ============================================================

def session_timeout_view(request):
    logout(request)

    return redirect("login")


# ============================================================
# SOIL HEALTH AND ASSESSMENT UPLOAD
# ============================================================
@login_required(login_url="login")
def soil_health_view(request):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "farmer":
        messages.error(
            request,
            "Only farmers can submit soil assessments."
        )
        return redirect("home")

    farms = Farm.objects.filter(
        farmer=request.user
    ).order_by("farm_name")

    if request.method == "POST":
        farm_id = request.POST.get("farm")
        assessment_type = request.POST.get("assessment_type")
        assessment_date = (
            request.POST.get("assessment_date") or None
        )
        reason = request.POST.get("reason")
        notes = request.POST.get("notes", "").strip()
        soil_file = request.FILES.get("soil_file")

        farm = (
            farms.filter(id=farm_id).first()
            if farm_id
            else None
        )

        allowed_types = dict(
            SoilAssessment.ASSESSMENT_TYPE_CHOICES
        )
        allowed_reasons = dict(
            SoilAssessment.REASON_CHOICES
        )

        if not farm:
            messages.error(
                request,
                "Please select a valid farm."
            )

        elif assessment_type not in allowed_types:
            messages.error(
                request,
                "Please select a valid assessment type."
            )

        elif reason not in allowed_reasons:
            messages.error(
                request,
                "Please select a valid reason."
            )

        elif not soil_file:
            messages.error(
                request,
                "Please upload a soil report."
            )

        elif soil_file.size > 10 * 1024 * 1024:
            messages.error(
                request,
                "The file must be 10 MB or smaller."
            )

        elif not soil_file.name.lower().endswith(
            (".pdf", ".jpg", ".jpeg", ".png")
        ):
            messages.error(
                request,
                "Upload a PDF, JPG, JPEG, or PNG file."
            )

        else:
            SoilAssessment.objects.create(
                farmer=request.user,
                farm=farm,
                assessment_type=assessment_type,
                assessment_date=assessment_date,
                reason=reason,
                notes=notes,
                soil_file=soil_file,
            )

            messages.success(
                request,
                "Your soil assessment was saved successfully."
            )
            return redirect("soil_health")

    assessments = SoilAssessment.objects.filter(
        farmer=request.user
    ).select_related(
        "farm"
    ).order_by("-created_at")

    # Get recommendations that professionals have sent
    # for this farmer's soil assessments.
    recommendations = SoilRecommendation.objects.filter(
        assessment__farmer=request.user,
        status="sent",
    ).select_related(
        "assessment",
        "professional",
        "assessment__farm",
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/soil_health.html",
        {
            "farms": farms,
            "assessments": assessments,
            "recommendations": recommendations,
        },
    )

# CREATE SOIL RECOMMENDATION

@login_required(login_url="login")
def create_soil_recommendation_view(request, assessment_id):
    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "agri_professional":
        messages.error(
            request,
            "Only agricultural professionals can provide recommendations."
        )
        return redirect("home")

    assessment = get_object_or_404(
        SoilAssessment.objects.select_related(
            "farmer",
            "farm",
        ),
        pk=assessment_id,
    )

    # Reuse this professional's existing draft for this assessment.
    recommendation = SoilRecommendation.objects.filter(
        assessment=assessment,
        professional=request.user,
        status="draft",
    ).order_by("-created_at").first()

    if request.method == "POST":
        form = SoilRecommendationForm(
            request.POST,
            instance=recommendation,
        )

        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.assessment = assessment
            recommendation.professional = request.user

            action = request.POST.get("action", "draft")

            if action == "send":
                recommendation.status = "sent"
                recommendation.sent_at = timezone.now()
                recommendation.save()

                assessment.status = "reviewed"
                assessment.save(update_fields=["status"])

                messages.success(
                    request,
                    "Your recommendation has been sent to the farmer."
                )
            else:
                recommendation.status = "draft"
                recommendation.save()

                messages.success(
                    request,
                    "Your recommendation has been saved as a draft."
                )

            return redirect(
                "professional_farmer_detail",
                farmer_id=assessment.farmer_id,
            )

    else:
        form = SoilRecommendationForm(
            instance=recommendation,
        )

    return render(
        request,
        "dashboard/soil_recommendation_form.html",
        {
            "form": form,
            "assessment": assessment,
            "recommendation": recommendation,
        },
    )
@login_required(login_url="login")
def send_soil_recommendation_view(request, recommendation_id):
    if request.method != "POST":
        return redirect("professional_farmers")

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != "agri_professional":
        messages.error(
            request,
            "Only agricultural professionals can send recommendations."
        )
        return redirect("home")

    recommendation = get_object_or_404(
        SoilRecommendation.objects.select_related(
            "assessment",
            "assessment__farmer",
        ),
        pk=recommendation_id,
        professional=request.user,
        status="draft",
    )

    recommendation.status = "sent"
    recommendation.sent_at = timezone.now()
    recommendation.save(
        update_fields=["status", "sent_at", "updated_at"]
    )

    assessment = recommendation.assessment
    assessment.status = "reviewed"
    assessment.save(update_fields=["status"])

    messages.success(
        request,
        "The existing recommendation has been sent to the farmer."
    )

    return redirect(
        "professional_farmer_detail",
        farmer_id=assessment.farmer_id,
    )