import datetime as dt

from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
    )

from .forms import CreateOrEditPostForm, EditProfileForm, CommentForm
from .models import Category, Post, Comment


User = get_user_model()


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        Post.comment_count += 1
    return redirect('blog:post_detail', pk=pk)


class EditComment(UpdateView):
    model = Comment
    form_class = CommentForm


class DeleteComment(DeleteView):
    pass


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all(
        ).filter(
            pub_date__lt=(dt.datetime.now()),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreateOrEditPostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreateOrEditPostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied('Вы не можете редактировать чужие записи')
        return super().dispatch(request, *args, **kwargs)


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied('Вы не можете удалять чужие записи')
        return super().dispatch(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(is_published=True),
            Q(category__is_published=True),
            Q(pub_date__lt=(dt.datetime.now()))
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        context['post'] = post
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


class CategoryPosts(ListView):
    model = Post, Category
    template_name = 'blog/category.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Post.objects.filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lt=(dt.datetime.now())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        posts = Post.objects.all().filter(category__slug=category_slug).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context


class Profile(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        posts = Post.objects.all().filter(author__username=username).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class EditProfile(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
