from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from core.query_sets import post_query
from .models import Post, Comment
from .forms import PostForm, CommentForm

User = get_user_model()

POSTS_PER_PAGE = 5


def index(request):
    """Выводит записи на главную."""
    template = "blog/index.html"
    post_list = post_query()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


def post_detail(request, id):
    """Выводит отдельную страницу поста."""
    template = "blog/detail.html"
    post = get_object_or_404(post_query(), pk=id)
    comments = post.comments.select_related('author')
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Выводит страницу категории."""
    from core.query_sets import category_query
    template = "blog/category.html"
    category = get_object_or_404(
        category_query(),
        slug=category_slug,
    )
    post_list = post_query().filter(
        category__slug=category_slug
    )
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)


@login_required
def post_create(request):
    """Создание публикации."""
    template = "blog/create.html"
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(
                'blog:profile', username=request.user.username
            )
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, template, context)


@login_required
def post_edit(request, id):
    """Редактирование публикации."""
    template = "blog/create.html"
    post = get_object_or_404(Post, pk=id)
    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)
    if request.method == 'POST':
        form = PostForm(
            request.POST, request.FILES, instance=post
        )
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    context = {"form": form, "post": post}
    return render(request, template, context)


@login_required
def post_delete(request, id):
    """Удаление публикации."""
    post = get_object_or_404(Post, pk=id)
    if request.user != post.author:
        return redirect('blog:post_detail', id=post.id)
    if request.method == 'POST':
        post.delete()
        return redirect(
            'blog:profile', username=request.user.username
        )
    context = {"post": post, "is_delete_confirm": True}
    return render(request, 'blog/detail.html', context)


@login_required
def add_comment(request, id):
    """Добавление комментария."""
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('blog:post_detail', id=post.id)


@login_required
def edit_comment(request, id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post_id=id
    )
    if request.user != comment.author:
        return redirect('blog:post_detail', id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentForm(instance=comment)
    context = {
        "post": comment.post,
        "form": form,
        "comment": comment,
        "is_edit_comment": True,
    }
    return render(request, 'blog/detail.html', context)


@login_required
def delete_comment(request, id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(
        Comment, pk=comment_id, post_id=id
    )
    if request.user != comment.author:
        return redirect('blog:post_detail', id=id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=id)
    context = {
        "post": comment.post,
        "comment": comment,
        "is_delete_comment_confirm": True,
    }
    return render(request, 'blog/detail.html', context)


def profile(request, username):
    """Страница пользователя."""
    template = "registration/profile.html"
    profile_user = get_object_or_404(User, username=username)
    if request.user == profile_user:
        post_list = Post.objects.filter(
            author=profile_user
        ).select_related('category', 'location')
    else:
        post_list = post_query().filter(author=profile_user)
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"profile": profile_user, "page_obj": page_obj}
    return render(request, template, context)


@login_required
def profile_edit(request, username):
    """Редактирование профиля."""
    template = "registration/profile_edit.html"
    if request.user.username != username:
        return redirect('blog:profile', username=username)
    if request.method == 'POST':
        request.user.first_name = request.POST.get(
            'first_name', ''
        )
        request.user.last_name = request.POST.get(
            'last_name', ''
        )
        request.user.email = request.POST.get('email', '')
        request.user.save()
        return redirect('blog:profile', username=username)
    context = {"profile": request.user}
    return render(request, template, context)


def signup(request):
    """Регистрация."""
    from django.contrib.auth.forms import UserCreationForm
    template = "registration/signup.html"
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, template, context)
