from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from django_extensions.db.models import AutoSlugField

from blog.validators import validate_title

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, validators=[validate_title])
    slug = AutoSlugField(populate_from='title', unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to="img/%Y/%m/%d/")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.title

    def is_liked_by(self, user) -> bool:
        return PostLike.objects.filter(post=self, user=user).exists()

    def is_disliked_by(self, user) -> bool:
        return PostDislike.objects.filter(post=self, user=user).exists()

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CharField,
                               related_name='comments')
    body = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-update_at', '-create_at')
        indexes = [
            models.Index(fields=['-update_at', '-create_at']),
        ]

    def __str__(self):
        return f'{self.author} - {self.post.title}'

    def is_liked_by(self, user) -> bool:
        return CommentLike.objects.filter(comment=self, user=user).exists()

    def is_disliked_by(self, user) -> bool:
        return CommentDislike.objects.filter(comment=self, user=user).exists()


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f'{self.user} - {self.post}'


class PostDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_dislikes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="dislikes")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f'{self.user} - {self.post}'


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "comment"]

    def __str__(self):
        return f'{self.user} - {self.comment}'


class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_dislikes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="dislikes")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "comment"]

    def __str__(self):
        return f'{self.user} - {self.comment}'
