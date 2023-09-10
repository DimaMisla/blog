from django import forms

from weather.models import Weather


class AddForm(forms.ModelForm):
    city = forms.CharField(max_length=50, label='city')


    class Meta:
        model = Weather
        fields = ['city']
