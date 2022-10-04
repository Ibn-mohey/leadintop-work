"""ad_library_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import logout
from re import template
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register,name = 'register'),
    path('login/', user_views.login_method, name = 'login'),
    path('logout/', user_views.logout_method ,name = 'logout'),
    path('users/', user_views.all_users ,name = 'users_page'),
    path('user/<email>/', user_views.change_profile, name='user_page'),
    # path('profile/', user_views.profile,name = 'profile'),
    path('', include('ad.urls')),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
