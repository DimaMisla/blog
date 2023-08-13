from django.contrib import admin

from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'info')
    list_filter = ('user', 'gender', 'date_of_birth')
    search_fields = ('user',)
