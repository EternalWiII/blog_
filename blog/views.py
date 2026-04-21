from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm


def post_list(request):
    query = request.GET.get('q', '')
    tag_slug = request.GET.get('tag', '')

    posts = Post.objects.filter(status='published').select_related('author', 'author__profile')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'tags': tags,
        'active_tag': active_tag,
        'query': query,
    })


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )
    comments = post.comments.filter(is_active=True).select_related('author', 'author__profile')
    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Увійдіть, щоб залишити коментар.')
            return redirect('accounts:login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано!')
            return redirect(post.get_absolute_url())

    related_posts = Post.objects.filter(
        status='published',
        tags__in=post.tags.all()
    ).exclude(pk=post.pk).distinct()[:3]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    })


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(status='published', tags=tag).select_related('author', 'author__profile')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag,
        'page_obj': page_obj,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Пост створено!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Створити'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете редагувати цей пост.')
        return redirect(post.get_absolute_url())
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост оновлено!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'action': 'Оновити'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете видалити цей пост.')
        return redirect(post.get_absolute_url())
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост видалено.')
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        messages.error(request, 'Ви не можете видалити цей коментар.')
    else:
        post_url = comment.post.get_absolute_url()
        comment.delete()
        messages.success(request, 'Коментар видалено.')
        return redirect(post_url)
    return redirect(comment.post.get_absolute_url())


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})
