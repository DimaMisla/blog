from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .models import Post, Comment, PostLike, PostDislike, CommentDislike, CommentLike, Category
from .forms import CommentForm, PostForm
from .utils import paginate_queryset, get_request_params

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        categories = self.request.GET.getlist('categories')
        date_end = self.request.GET.get('date_end', None)
        user = self.request.GET.get('user', None)

        if user:
            queryset = queryset.filter(author__username=user)

        if categories:
            queryset = queryset.filter(category__name__in=categories)

        if date_end:
            queryset = queryset.filter(update_at__gte=date_end)

        keyword = self.request.GET.get('keyword', )
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        per_page = self.request.GET.get('per_page', self.paginate_by)
        paginator = Paginator(context['posts'], per_page)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)
        query_string = self.request.GET.urlencode()

        context.update({
            'title': 'Home page',
            'posts': posts,
            'total_pages': paginator.num_pages,
            'query_string': query_string,

        })

        return context


class PostSearchView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get_context('search', )

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))

        return queryset


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


# def search_posts(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('search', '')
#         post = Post.objects.filter(title__icontains=search_query)
#         first_post = post.first()
#         if post:
#             return redirect('blog:post_detail', slug=first_post.slug)
#
#     return redirect('blog:home')
