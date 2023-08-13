from django import forms
from django.core.validators import FileExtensionValidator

from blog.models import Comment, Post
from blog.validators import validate_file_size


class PostForm(forms.ModelForm):
    image = forms.ImageField(validators=[
        validate_file_size,
        FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])
    ])

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category']


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('body',)


