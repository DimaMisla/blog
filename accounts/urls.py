from django.urls import path, reverse

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('profile/subscribe/<int:pk>/', views.toggle_subscribe, name='subscribe'),
    path('profile/unsubscribe/<int:pk>/', views.toggle_subscribe, name='unsubscribe'),
]

