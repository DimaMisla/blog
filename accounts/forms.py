from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from accounts.models import Profile
from blog.validators import validate_file_size


class DefaultProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )

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


class CustomAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Mail..'}), label='E-Mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password..'}), label='Password')

    class Meta:
        model = User
        fields = ['email', 'password']
