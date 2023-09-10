from django.urls import path, reverse

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('profile/subscribe/<int:pk>/', views.toggle_subscribe, name='subscribe'),
    path('profile/unsubscribe/<int:pk>/', views.toggle_subscribe, name='unsubscribe'),
]
