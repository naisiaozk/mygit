from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^index/$", views.index, name="index"),
    url(r"^login/$", views.login, name="login"),
    url(r"^register/$", views.register, name="register"),

    url(r"^show_article/$", views.show_article, name="show_article"),
    url(r"^article_list/(\d+)/$", views.article_list, name="article_list"),
    url(r"^article_list/$", views.article_list, name="article_list"),

    url(r"^article_publish/$", views.article_publish, name="article_publish"),
    url(r"^article_update/$", views.article_update, name="article_update"),
    url(r"^code/$", views.code, name="code"),

    url(r"^(?P<a_id>\d+)/show_article/$", views.show_article, name="show_article"),
    # url(r"^article_list/$", views.article_list, name="article_list"),
    url(r"^(?P<a_id>\d+)/article_update/$", views.article_update, name="article_update"),

]