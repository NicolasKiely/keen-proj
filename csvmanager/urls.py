from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^upload$', views.upload, name='upload'),
    url(r'^document$', views.document, name='document'),
    url(r'^post_upload$', views.post_upload, name='post_upload'),
    url(r'', views.index, name='index')
]
