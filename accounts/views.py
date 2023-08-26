from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods

from accounts.forms import DefaultProfileForm, CustomUserCreationForm, EditProfileForm, CustomAuthenticationForm
from accounts.models import Profile, ProfileSubscription
from blog.models import Post

from datetime import datetime, date


User = get_user_model()

def login_request(request):
    form = CustomAuthenticationForm()

    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            try:
                user = get_object_or_404(User, email=form.cleaned_data['email'])
                if user.check_password(form.cleaned_data['password']):
                    login(request, user)
                    return redirect("blog:home")
            except User.DoesNotExist:
                return render(request=request, template_name="accounts/login.html", context={"form": form})
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


def profile(request, pk):
    user_profile = get_object_or_404(Profile, user=pk)
    user_posts = Post.objects.filter(author=pk)
    context = {
        'profile': user_profile,
        'user_posts': user_posts,
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
            return redirect('accounts:profile', pk=pk)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'accounts/profile/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def toggle_subscribe(request, pk):
    profile_user = get_object_or_404(Profile, user=pk)
    if profile_user.user == request.user:
        return redirect('accounts:profile', pk=pk)
    profile_subscription, created = ProfileSubscription.objects.get_or_create(
        user=request.user,
        profile=profile_user,
    )
    if not created:
        profile_subscription.delete()

    return redirect('accounts:profile', pk=pk)

