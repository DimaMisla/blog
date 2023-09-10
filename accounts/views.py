from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from accounts.forms import DefaultProfileForm, EditProfileForm, RegisterForm, ProfileForm
from accounts.models import Profile, ProfileSubscription
from blog.models import Post


User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('blog:home')

    def get_success_url(self):
        return self.success_url


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class RegisterView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blog:home')


class ProfileCreateView(FormView):
    template_name = 'accounts/profile/profile_create.html'
    form_class = ProfileForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)


class ProfileView(View):
    def get(self, request, pk):
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

