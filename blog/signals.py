import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from blog.models import Post


@receiver(pre_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    path = instance.image.path
    if os.path.exists(path):
        os.remove(path)

