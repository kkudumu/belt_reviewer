from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'process_addbook$', views.process_addbook),
    url(r'register$', views.register),
    url(r'bookspage$', views.bookspage),
    url(r'login$', views.login),
    url(r'logout$', views.logout),
    url(r'addbook$', views.display_addbook),
    url(r'book/(?P<id>\d+)$', views.display_book),
    url(r'process_review/(?P<id>\d+)$', views.process_review),
    url(r'user/(?P<id>\d+)$', views.display_user),
    url(r'remove$', views.remove),
]