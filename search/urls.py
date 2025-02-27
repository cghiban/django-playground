from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("check-task", views.check_task, name="check_task"),
    path("search-results", views.search_results, name="search_results")
]
