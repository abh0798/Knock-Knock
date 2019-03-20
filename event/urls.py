"""knock_knock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main),
    path('event/<int:ID>/', views.event),
    path('rules/', views.rules),
    path('special/', views.special),
    path('leaderboard/', views.leader),
    path('winners/', views.winners),
    path('signup/', views.signup),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='password.html'), name='password_reset_confirm'),
    path('reset/done/', views.reset_done, name='password_reset_complete'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(template_name='signin.html'), name = 'login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)