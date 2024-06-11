from django.urls import path
from store import views

urlpatterns = [
    path("product/", views.product_list),
    path("product/<int:id>/", views.product_details),  # <int:id> only accept integers
    path("collection/<int:pk>", views.collection_detail, name='collection-detail'),
]
