from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User
from .constants import POSTS_PAGE


def index(request):
    """View функция для index."""
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """View функция для group_posts."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """View функция для profile."""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """View функция для post_detail."""
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """View функция для создания записи."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()

            return redirect(f'/profile/{form.author.username}/')

        return render(request, 'posts/create_post.html', {'form': form})

    form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """View функция для редактирования записи."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id != post.author_id:

        return redirect('posts:post_detail', pk=post_id)

    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()

            return redirect('posts:post_detail', post_id=post_id)

    else:
        form = PostForm(instance=post)
    context = {
        'post_id': post_id,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)
