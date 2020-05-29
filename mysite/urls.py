from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Video_list, name='home'),
    path('Video/', views.Video_list, name='Video_list'),
    path('Video/upload/', views.upload_Video, name='upload_Video'),
    path('Video/<int:pk>/', views.delete_Video, name='delete_Video'),
    path('view_Video/<int:pk>/', views.view_Video, name='view_Video'),
    path('admin/', admin.site.urls),
    path('test/', views.test,name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    