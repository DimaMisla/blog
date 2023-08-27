from django import template

register = template.Library()


@register.filter
def subscribe(entity, user) -> bool:
    if not user.is_authenticated:
        return False
    return entity.subscribe(user)
