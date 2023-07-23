from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, CreateOrEditPostForm
from .models import Category, Comment, Post

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
        post.comment_count += 1
        post.save()
    return redirect('blog:post_detail', pk=pk)


class EditComment(LoginRequiredMixin, UpdateView):

    def get(self, request, pk, pk2):
        comment = get_object_or_404(Comment, post_id=pk, id=pk2)
        if comment.author != request.user:
            raise PermissionDenied(
                'Вы не можете редактировать чужие комментарии'
            )
        form = CommentForm(instance=comment)
        context = {
            'form': form,
            'comment': comment,
        }
        return render(request, 'blog/comment.html', context=context)

    def post(self, request, pk, pk2):
        comment = Comment.objects.get(post_id=pk, id=pk2)
        if comment.author != request.user:
            raise PermissionDenied
        form = CommentForm(request.POST, instance=comment)
        context = {
            'form': form,
            'comment': comment,
        }
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
        else:
            return render(request, 'blog/comment.html', context=context)


class DeleteComment(LoginRequiredMixin, DeleteView):
    def get(self, request, pk, pk2):
        comment = get_object_or_404(Comment, post_id=pk, id=pk2)
        if comment.author != request.user:
            raise PermissionDenied('Вы не можете удалять чужие комментарии')
        return render(request, 'blog/comment.html', {'comment': comment})

    def post(self, request, pk, pk2):
        post = get_object_or_404(Post, pk=pk)
        comment = Comment.objects.get(post_id=pk, id=pk2)
        if comment.author != request.user:
            raise PermissionDenied
        comment.delete()
        post.comment_count -= 1
        post.save()
        return redirect('blog:post_detail', pk=pk)


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all(
        ).filter(
            pub_date__lt=(timezone.now()),
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
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreateOrEditPostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
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
        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(author=self.request.user)
                | Q(
                    is_published=True,
                    category__is_published=True,
                    pub_date__lt=(timezone.now())
                )
            )
        return queryset.filter(
            Q(is_published=True),
            Q(category__is_published=True),
            Q(pub_date__lt=(timezone.now()))
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
            pub_date__lt=(timezone.now())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        posts = Post.objects.all().filter(
            category__slug=category_slug,
            pub_date__lt=(timezone.now()),
            is_published=True,
            category__is_published=True,
        ).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['category'] = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True,
        )
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
        posts = Post.objects.all(
        ).filter(author__username=username
                 ).order_by('-pub_date')
        visible_posts = []
        for post in posts:
            if post.is_published and (post.pub_date <= timezone.now()
                                      ) or (self.request.user == post.author):
                visible_posts.append(post)
        paginator = Paginator(visible_posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})
