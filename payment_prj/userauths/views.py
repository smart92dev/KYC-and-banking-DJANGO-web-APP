from django.shortcuts import render, redirect
from userauths.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def RegisterView(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("core:index")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("core:index")

    context = {
        "form": form
    }

    return render(request, "userauths/sign-up.html", context)

def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("userauths:sign-in")
        except User.DoesNotExist:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("account:account")

    return render(request, "userauths/sign-in.html")

def logoutView(request):
    logout(request.user)
    messages.success(request, "You have been logged out.")
    return redirect("userauths:sign-in")

