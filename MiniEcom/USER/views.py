from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("product_list")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login_user")

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, "profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})

@login_required
def delete_user(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Account deleted successfully.")
        return redirect("register_user")
    return render(request, "confirm_delete.html")
