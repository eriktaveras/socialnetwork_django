# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView,CreateView, ListView, FormView, RedirectView
from usuarios.models import Post, Comment
from usuarios.forms import PostForm, RegistrationForm, LoginForm, CommentForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from friendship.models import Friend, Follow, Block

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['form'] = PostForm()
        return context

# def post_detail(request, id):
#     template_name = 'post_detail.html'
#     post = get_object_or_404(Post, id=id)
#     comments = get_object_or_404(Comment, id=id)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():

#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})

class PostViewDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-date_create')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        def get_context_data(self, **kwargs):
            data = super().get_context_data(**kwargs)
            likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
            liked = False
            if likes_connected.likes.filter(id=self.request.user.id).exists():
                liked = True
            data['number_of_likes'] = likes_connected.number_of_likes()
            data['post_is_liked'] = liked
            likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
            liked = False
            if likes_connected.likes.filter(id=self.request.user.id).exists():
                liked = True
            data['number_of_likes'] = likes_connected.number_of_likes()
            data['post_is_liked'] = liked

        return data
    
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),user=self.request.user, post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
    # def post(self, request, **kwargs):
    #     post = Post.objects.get(pk=self.kwargs.get("pk"))
    #     form = self.form(request.POST or None, instance=post)
    #     if form.is_valid():
    #         form.save()
    #     return reverse('post-detail', kwargs={'pk': post.pk})

        # def form_valid(self,form,*args,**kwargs):
        # self.object = form.save(commit = False)
        # self.object.user = self.request.user
        # self.object.save()
        # return super().form_valid(form)

class PostFormView(FormView):
    template_name = 'home.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class PostView(TemplateView):
    template_name = 'post.html'

class SignUpView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'register.html'
    success_url = reverse_lazy( 'home' )

class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super (LogOutView, self).get(request, *args, **kwargs)


# class Profile(DetailView):
#     template_name = 'profile.html'
#     model = User
#     def get_object(self, queryset=None):
#         return self.request.user

def profile(request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
            posts=Post.objects.filter(user=request.user)

        else:
            user = request.user
            posts=Post.objects.filter(user=request.user)
        return render(request, 'profile.html', {'user': user, 'posts': posts})


def BlogPostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def lista_usuarios(request):
    amigos = Friend.objects.friends(request.user)
    followers = Follow.objects.followers(request.user)
    followings =Follow.objects.following(request.user) 
    friendship_requests = Friend.objects.requests(request.user)
    context = {'amigos': amigos,
               'followers': followers,
               'followings': followings,
               'friendship_requests' : friendship_requests}

    return render(request, 'lista_usuarios.html', context)


