from django.urls import path, reverse

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_pk>/', views.profile, name='profile'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
]

