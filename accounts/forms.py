from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from accounts.models import Profile
from accounts.validators import validate_birth_date
from blog.validators import validate_file_size

User = get_user_model()


class DateInputCustom(forms.DateInput):
    input_type = 'date'


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


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'avatar', 'bio', 'info')

        labels = {
            'date_of_birth': 'Date of your Birth',
            'avatar': 'Avatar URL'
        }

        placeholders = {
            'avatar': 'Left empty to use gravatar',
            'bio': 'Write a short biography',
            'info': 'Enter some additional information'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': self.Meta.placeholders.get(field_name)})
        self.fields['date_of_birth'].widget = DateInputCustom()

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        try:
            validate_birth_date(data)
        except ValidationError as exception:
            self.add_error('date_of_birth', str(exception))
        return data
