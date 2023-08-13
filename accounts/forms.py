from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from accounts.models import Profile
from blog.validators import validate_file_size


class DefaultProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "date_of_birth"]


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(validators=[
        validate_file_size,
        FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        required=False
    )

    class Meta:
        model = Profile
        fields = ["bio", "info"]

    bio = forms.CharField(required=False)
    info = forms.CharField(required=False)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
