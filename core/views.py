from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db import IntegrityError

from .models import (
    Athlete,
    UserProfile,
    InjuryReport,
    TrainingSession,
    Availability
)

from .logic import match_score


# <!---------------------------------HOME / STATIC PAGES--------------------------------->

def home(request):
    if request.user.is_authenticated:
        return redirect("welcome")

    return render(request, "home.html")


def landing(request):
    return render(request, "landing.html")


def about(request):
    return render(request, "aboutus.html")


def contact(request):
    return render(request, "contactus.html")


# <!---------------------------------SIGNUP--------------------------------->

def signup(request):
    error = None

    if request.method == "POST":
        try:
            # Create Django user
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"]
            )

    
            role = request.POST["role"]
            gym = request.POST["gym"]

            # Create user profile
            UserProfile.objects.create(
                user=user,
                role=role,
                gym=gym
            )

            # Only athletes need athlete stats
            if role == "Athlete":
                Athlete.objects.create(
                    user=user,
                    age=request.POST.get("age") or 0,
                    weight=request.POST.get("weight") or 0,
                    height=request.POST.get("height") or 0,
                    discipline=request.POST.get("discipline", ""),
                    skill_level=request.POST.get("skill_level") or 0,
                    experience_years=request.POST.get("experience_years") or 0,
                    injury_status=False
                )

            return render(request, "signup.html", {
                "success": True
            })

        except IntegrityError:
            error = "Username already exists"

    return render(request, "signup.html", {
        "error": error
    })


#<!--------------------------------- PROFILE --------------------------------->

@login_required
def profile(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    return render(request, "profile.html", {
        "profile": profile
    })


# <---------------------------------WELCOME PAGE--------------------------------->

@login_required
def welcome(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    return render(request, "welcome.html", {
        "profile": profile
    })


# <!---------------------------------ATHLETE DASHBOARD--------------------------------->

@login_required
def athlete_dashboard(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != "Athlete":
        return redirect("welcome")

    return render(request, "athlete_dashboard.html")


@login_required
def dashboard(request):
    return render(request, "athletedashboard.html")


# <!--------------------------------- COACH DASHBOARD --------------------------------->

@login_required
def coach_dashboard(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # Only coaches should access
    if profile.role != "Coach":
        return redirect("welcome")

    # Users in same gym
    gym_users = UserProfile.objects.filter(
        gym=profile.gym
    ).values_list("user", flat=True)

    # Athletes in same gym
    athletes = Athlete.objects.filter(
        user__in=gym_users
    )

    injuries = InjuryReport.objects.filter(
        athlete__user__in=gym_users
    ).order_by("-id")

    # <!------------------------- Matchmaking logic ------------------------->

    recommendations = []
    athlete_list = list(athletes)

    for i in range(len(athlete_list)):
        for j in range(i + 1, len(athlete_list)):
            athlete_1 = athlete_list[i]
            athlete_2 = athlete_list[j]

            score, reason = match_score(
                athlete_1,
                athlete_2
            )

            recommendations.append({
                "a1": athlete_1,
                "a2": athlete_2,
                "score": score,
                "reason": reason
            })

    # Highest score first
    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Injury reports
    injuries = InjuryReport.objects.filter(
        athlete__user__userprofile__gym=profile.gym
    )

    # Training logs
    training_logs = TrainingSession.objects.filter(
        athlete__user__in=gym_users
    ).order_by("-date")

    return render(request, "coachdashboard.html", {
        "athletes": athletes,
        "recommendations": recommendations,
        "injuries": injuries,
        "training_logs": training_logs
    })


# <!---------------------------------INJURY REPORTING--------------------------------->

@login_required
def submit_injury(request):
    athlete = get_object_or_404(
        Athlete,
        user=request.user
    )

    if request.method == "POST":
        InjuryReport.objects.create(
            athlete=athlete,
            injury_type=request.POST["injury_type"],
            severity=request.POST["severity"],
            description=request.POST["description"]
        )

        messages.success(
            request,
            "Injury report submitted successfully."
        )

        return redirect("/injury/")

    return render(request, "injuryform.html")


# <!--------------------------------- MATCH RECOMMENDATIONS --------------------------------->

@login_required
def recommendations(request):
    athlete = get_object_or_404(
        Athlete,
        user=request.user
    )

    others = Athlete.objects.exclude(
        id=athlete.id
    )

    results = []

    for other in others:
        score, reason = match_score(
            athlete,
            other
        )

        if score == 2:
            label = "Safe"
        elif score == 1:
            label = "Medium Risk"
        else:
            label = "Unsafe"

        results.append({
            "athlete": other,
            "score": score,
            "label": label,
            "reason": reason
        })

    return render(request, "recommendations.html", {
        "athlete": athlete,
        "results": results
    })


# <!---------------------------------TRAINING LOG--------------------------------->

@login_required
def log_training(request):
    athlete = get_object_or_404(
        Athlete,
        user=request.user
    )

    if request.method == "POST":
        TrainingSession.objects.create(
            athlete=athlete,
            discipline=request.POST["discipline"],
            duration=request.POST["duration"],
            intensity=request.POST["intensity"],
            notes=request.POST["notes"]
        )

        messages.success(
            request,
            "Training session logged successfully."
        )

        return redirect("/log-training/")

    sessions = TrainingSession.objects.filter(
        athlete=athlete
    ).order_by("-date")

    return render(request, "logtraining.html", {
        "sessions": sessions
    })


# <!---------------------------------COACH INJURY VIEW--------------------------------->

@login_required
def coach_injuries(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    injuries = InjuryReport.objects.filter(
        athlete__user__userprofile__gym=profile.gym
    )

    return render(request, "coach_injuries.html", {
        "injuries": injuries
    })


# <!---------------------------------TRAINING LOAD--------------------------------->

@login_required
def training_load(request):
    athlete = get_object_or_404(
        Athlete,
        user=request.user
    )

    sessions = TrainingSession.objects.filter(
        athlete=athlete
    )

    total_week = sum(
        session.duration for session in sessions
    )

    return render(request, "training_load.html", {
        "sessions": sessions,
        "total_week": total_week
    })


# <!--------------------------------- AVAILABILITY--------------------------------->

@login_required
def availability(request):
    athlete = get_object_or_404(
        Athlete,
        user=request.user
    )

    if request.method == "POST":
        Availability.objects.create(
            athlete=athlete,
            date=request.POST["date"],
            available=True
        )

        return redirect("/dashboard/")

    return render(request, "availability.html")


#<! --------------------------------- LOGOUT --------------------------------->

def logout_user(request):
    logout(request)
    request.session.flush()

    return redirect("home")


#<! ---------------------------------LOGIN REDIRECT--------------------------------->

def post_login_redirect(user):
    if hasattr(user, "userprofile"):

        if user.userprofile.role == "Coach":
            return redirect("coach_dashboard")

        return redirect("dashboard")

    return redirect("home")