from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_category_list_page, name="list-category"),
    path("addc/", views.add_category, name="add-category"),
    path("editc/", views.edit_category, name="edit-category"),
    path("deletec/", views.delete_category, name="delete-category"),
]
