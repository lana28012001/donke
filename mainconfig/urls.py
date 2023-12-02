"""newautohost URL Configuration

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
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns = [
#     path('', include('core.urls')),
#     path('admin/', admin.site.urls),
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from core import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
    # url('', views.handler503),
    url('', include('core.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', favicon_view),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
            
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.views.handler404'
handler500 = 'core.views.views.handler500'
