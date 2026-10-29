from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("professional/soil-recommendations/<int:recommendation_id>/send/", views.send_soil_recommendation_view, name="send_soil_recommendation"),
    path(
        "farmer-dashboard/",
        views.farmer_dashboard_view,
        name="farmer_dashboard",
    ),

    path("add-farm/", views.add_farm_view, name="add_farm"),
    path("my-farms/", views.my_farms_view, name="my_farms"),

    
    path("soil_health/", views.soil_health_view, name="soil_health"),
    path(
        "agri-professional-dashboard/",
        views.agri_professional_dashboard_view,
        name="agri_professional_dashboard",
    ),
    
    path(
        "professional/farmers/",
        views.professional_farmers_view,
        name="professional_farmers",
    ),
    path(
        "professional/farmers/<int:farmer_id>/",
        views.professional_farmer_detail_view,
        name="professional_farmer_detail",
    ),
    path(
        "professional/profile/",
        views.professional_profile_view,
        name="professional_profile",
    ),
    path(
        "professional/soil-assessments/<int:assessment_id>/recommendation/",
        views.create_soil_recommendation_view,
        name="create_soil_recommendation",
    ),

    path(
        "session_timeout/",
        views.session_timeout_view,
        name="session_timeout",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )