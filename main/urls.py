from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from usuarios.views import HomeView, PostView, LoginView, SignUpView, PostFormView, LogOutView, profile, PostViewDetail, BlogPostLike, lista_usuarios

urlpatterns = [
    path('admin/', admin.site.urls ),
    path('',login_required(HomeView.as_view(), login_url='login'), name='home'),
    path('profile/', profile, name='profile' ),
    path('login/', LoginView.as_view(), name='login' ),
    path('register/', SignUpView.as_view(), name='register' ),
    path('postform/', PostFormView.as_view(), name='postform' ),
    path('logout/', LogOutView.as_view(), name='logout' ),
    path('post/<str:pk>/', PostViewDetail.as_view(), name='post_detail'),
    path('blogpost-like/<int:pk>', BlogPostLike, name="blogpost_like"),
    path('friendship/', include('friendship.urls')),
    path('lista_usuarios/', lista_usuarios, name='lista_usuarios')

    

   

]
