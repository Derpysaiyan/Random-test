from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Member
# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def signup(request):
    if request.method == "POST":
        Member.objects.create(            
            firstname=request.POST.get("firstname"),
            lastname=request.POST.get("lastname"),
            age=int(request.POST.get("age")),
            email=request.POST.get("email"),
            password=make_password(request.POST.get("password")),
            experience=request.POST.get("experience"),
            goals=request.POST.get("goals"),)
        return redirect("homepage")
    return render(request, 'signup.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            member = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return HttpResponse("User not found")
        if check_password(password, member.password):
            request.session["member_id"] = member.id
            return redirect("homepage")
        else:
            return HttpResponse("Wrong password")
    return render(request, 'login.html')