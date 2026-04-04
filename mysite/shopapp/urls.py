from django.urls import path
from .views import product_list

app_name = "shopapp"
urlpatterns = [
    path("", product_list, name="index"),
]