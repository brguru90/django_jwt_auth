from django.conf.urls import include, url
from apis import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^login/$', views.login),
    url(r'^verify_login/$', views.verify_login),
]