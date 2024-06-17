from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('random_page/', views.random_page, name='random_page'),
    path("search/",views.search, name="search"),
    path("edit/", views.edit, name="edit"),
    path("save_edit", views.save_edit, name="save_edit"),
]
