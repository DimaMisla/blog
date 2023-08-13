from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from accounts.forms import DefaultProfileForm, CustomUserCreationForm, EditProfileForm
from accounts.models import Profile
from blog.models import Post

from datetime import datetime, date


def login_request(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("blog:home")

    return render(request=request, template_name="accounts/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    return redirect("blog:home")


def register(request):
    form = CustomUserCreationForm()
    profile_form = DefaultProfileForm()
    today = date.today()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        profile_form = DefaultProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)

            age = today.year - profile.date_of_birth.year - ((today.month, today.day) < (profile.date_of_birth.month, profile.date_of_birth.day))
            if age < 18:
                return render(request, 'accounts/registration.html', context={"form": form, "profile_form": profile_form})

            user = form.save()
            profile.user = user
            profile.bio = " "
            profile.info = " "
            profile.save()
            return redirect("accounts:login")

    context = {"form": form, "profile_form": profile_form, "years": range(1900, today.year)}
    return render(request, 'accounts/registration.html', context)


def profile(request, user_pk):
    user_profile = Profile.objects.get(user=user_pk)
    user_posts = Post.objects.filter(author=user_pk)
    context = {
        'profile': user_profile,
        'user_posts': user_posts
    }
    return render(request, 'accounts/profile/profile.html', context)


@login_required
def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.user != profile.user:
        raise PermissionDenied("You are not a profile owner")

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user_pk=pk)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'accounts/profile/edit_profile.html', {'form': form, 'profile': profile})

