"""askme_sysoev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.urls import path
from askme_sysoev import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('question/<int:id>/', views.question, name='question'),
    path('settings', views.settings, name='settings'),
    path('login', views.login, name='login'),
    path('signup', views.register, name='register'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:name>/', views.tag, name='tag'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload-image/', views.upload_image, name='upload_image'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
