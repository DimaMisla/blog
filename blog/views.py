from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Post, Comment, PostLike, PostDislike, CommentDislike, CommentLike
from .forms import CommentForm, PostForm
from .utils import paginate_queryset, get_request_params


def home(request):
    per_page = 4

    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', per_page)

    queryset = Post.objects.all()
    posts, total_pages = paginate_queryset(queryset, page, per_page)

    query_string = get_request_params(request)

    context = {
        'title': 'Home page',
        'maintainer': 'dima misla',
        'posts': posts,
        'total_pages': total_pages,
        'query_string': query_string
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post': post,
        'form': CommentForm(),
    }
    return render(request, 'blog/post/detail.html', context)


@login_required
def form_edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        raise PermissionDenied("You are not a post author")

    form = PostForm(instance=post)
    return render(request, 'blog/post/edit_post.html', {'form': form, 'post': post})


@require_http_methods(["POST"])
@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        raise PermissionDenied("You are not a post author")

    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', slug=post.slug)
    return render(request, 'blog/post/edit_post.html', {'form': form, 'post': post})


@login_required
def from_post(request):
    return render(request, 'blog/post/form_post.html', {'form': PostForm()})


@require_http_methods(["POST"])
@login_required
def add_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:home')

    context = {
        'form': form,
    }
    return render(request, 'blog/post/form_post.html', context)


@require_http_methods(["POST"])
@login_required
def add_post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)
    else:
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'blog/post/detail.html', context)


@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_like, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post,
    )
    if not created:
        post_like.delete()
    else:
        if post.is_disliked_by(request.user):
            post_dislike = PostDislike.objects.get(post=post, user=request.user)
            post_dislike.delete()
    return redirect('blog:post_detail', slug=post.slug)


@login_required
def toggle_post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_dislike, created = PostDislike.objects.get_or_create(
        user=request.user,
        post=post,
    )
    if not created:
        post_dislike.delete()
    else:
        if post.is_liked_by(request.user):
            post_like = PostLike.objects.get(post=post, user=request.user)
            post_like.delete()
    return redirect('blog:post_detail', slug=post.slug)


@login_required
def toggle_comment_like(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment_like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment,
    )
    if not created:
        comment_like.delete()
    else:
        if comment.is_disliked_by(request.user):
            comment_dislike = CommentDislike.objects.get(comment=comment, user=request.user)
            comment_dislike.delete()
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def toggle_comment_dislike(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment_dislike, created = CommentDislike.objects.get_or_create(
        user=request.user,
        comment=comment,
    )
    if not created:
        comment_dislike.delete()
    else:
        if comment.is_liked_by(request.user):
            comment_like = CommentLike.objects.get(comment=comment, user=request.user)
            comment_like.delete()
    return redirect('blog:post_detail', slug=comment.post.slug)


