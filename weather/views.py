import os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from weather.exceptions import CityNotFoundError, ExternalServiceError
from weather.forms import AddForm
from weather.models import Weather
from weather.services import CurrentWeatherService

User = get_user_model()


def widget(request):
    city = request.GET.get('city')
    if city is None:
        pass
    api_key = os.getenv('API_TOKEN')
    weather_dto = None
    error = None

    weather_service = CurrentWeatherService(api_key=api_key, units='metric')
    try:
        weather_dto = weather_service.get_weather(city_name=city)
    except CityNotFoundError as exception:
        error = str(exception)
    except ExternalServiceError as exception:
        error = 'External service error, please try again later'
    context = {
        'weather': weather_dto,
        'error': error
    }
    return render(request, 'weather/weather.html', context)


class CatalogView(LoginRequiredMixin, TemplateView):
    template_name = 'weather/search_city.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.user)
        context = {
            'cities': user.weather.all()
        }
        return context


# @login_required
# def toggle_add_city(request):
#     city, created = Weather.objects.get_or_create(
#         user=request.user,
#         city=request.f
#     )
#
#     return redirect(f'weather:widget?{city}')


# class AddView(TemplateView):
#     template_name = 'weather/add.html'
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'form': AddForm
#         }
#         return context


class AddView(FormView):
    template_name = 'weather/add.html'
    form_class = AddForm
    success_url = reverse_lazy('weather:catalog')

    def form_valid(self, form):
        weather_instance = form.save(commit=False)
        weather_instance.save()
        weather_instance.user.add(self.request.user)
        return super().form_valid(form)


def delete(request, slug):
    city = Weather.objects.filter(user=request.user, city=slug)
    city.delete()
    return redirect('weather:catalog')


# class WidgetView(View):
#
#     def get_context_data(self, **kwargs):
#         country = self.request.GET.get('country', '')
#         weather, temp, name = get_weather(country)
#         context = {
#             'weather': weather,
#             'temp': temp,
#             'name': name
#         }
#
#         return render(self.request, 'weather/weather.html', context)
