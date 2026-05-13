from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from .models import Member, Availability, Run
# Create your views here.

def homepage(request):
    member_id = request.session.get("member_id")
    return render(request, 'homepage.html', {"logged_in": member_id is not None})

def signup(request):
    member_id = request.session.get("member_id")

    if member_id:
        return redirect("/")

    if request.method == "POST":
        member = Member.objects.create(            
            firstname=request.POST.get("firstname"),
            lastname=request.POST.get("lastname"),
            age=int(request.POST.get("age")),
            email=request.POST.get("email"),
            password=make_password(request.POST.get("password")),
            experience=request.POST.get("experience"),
            goals=request.POST.get("goals"),)
        request.session["member_id"] = member.id
        return redirect("profile")
    return render(request, 'signup.html')

def profile(request):
    member_id = request.session.get("member_id")

    if not member_id:
        return redirect("login")

    member = Member.objects.get(id=member_id)

    if request.method == "POST":
        member.goals = request.POST.get("goals")
        member.experience = request.POST.get("experience")
        member.save()

        return redirect("profile") 

    availability = Availability.objects.filter(member=member)

    return render(request, 'profile.html', {
        "member": member,
        "availability": availability
    })

def add_availability(request):
    member_id = request.session.get("member_id")

    if not member_id:
        return redirect("login")

    member = Member.objects.get(id=member_id)

    if request.method == "POST":
        Availability.objects.update_or_create(
            member=member,
            defaults={
                "days": request.POST.get("days"),
                "times": request.POST.get("times")})
        return redirect("profile")

    return redirect("profile")

def login(request):
    member_id = request.session.get("member_id")

    if member_id:
        return redirect("profile")

    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            member = Member.objects.get(email=email)
        except Member.DoesNotExist:
            error = "No account found with that email"
            return render(request, "login.html", {"error": error})

        if check_password(password, member.password):
            request.session["member_id"] = member.id
            return redirect("profile")
        else:
            error = "Incorrect password"
            return render(request, "login.html", {"error": error})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def runs(request):
    member_id = request.session.get("member_id")

    if not member_id:
        return redirect("login")

    member = Member.objects.get(id=member_id)

    if request.method == "POST":
        Run.objects.create(
            member=member,
            distance=request.POST.get("distance"),
            duration=request.POST.get("duration")
        )
        return redirect("runs")

    runs = Run.objects.filter(member=member).order_by("created_at")

    total_runs = runs.count()

    if total_runs > 0:
        avg_distance = sum(r.distance for r in runs) / total_runs
        avg_duration = sum(r.duration for r in runs) / total_runs
        avg_pace = avg_duration / avg_distance

        labels = [r.created_at.strftime("%m-%d") for r in runs]
        distances = [r.distance for r in runs]
        durations = [r.duration for r in runs]
    else:
        avg_distance = avg_duration = avg_pace = 0
        labels = []
        distances = []
        durations = []

    context = {
        "runs": runs,
        "avg_distance": avg_distance,
        "avg_duration": avg_duration,
        "avg_pace": avg_pace,
        "labels": labels,
        "distances": distances,
        "durations": durations,
    }

    return render(request, "runs.html", context)