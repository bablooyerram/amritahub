"""amritahub URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
path('home/',views.home),
    path('signup/',views.signup1),
path('profile/',views.profilepage),
path('proedit/',views.profileEDIT),
path('message/',views.messages),
    path('uploadpost/',views.uploadphoto),
path('likepost/<int:postid>/', views.likepost),

#url(r'^comments/(?P<oid>[0-9]+)/$', views.comments, name='objects'),
    path('logout/',views.logout1),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html")),
  #  path('confirmemail/',views.emailconfirm),
   path('forgot/',views.forgot),
path('event/',views.event),
    path('friends/',views.friends),
    path('photos/',views.photos)
]
