from django import template

register = template.Library()


@register.filter
def is_liked_by(entity, user) -> bool:
    if not user.is_authenticated:
        return False
    return entity.is_liked_by(user)


@register.filter
def is_disliked_by(entity, user) -> bool:
    if not user.is_authenticated:
        return False
    return entity.is_disliked_by(user)

