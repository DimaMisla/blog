from django.contrib.auth import get_user_model

from .models import Category


User = get_user_model()


def get_search_objects(request):
    category_objects = Category.objects.all().order_by('name')
    users_objects = User.objects.all().order_by('username')
    return {'categories': category_objects, 'users': users_objects}
