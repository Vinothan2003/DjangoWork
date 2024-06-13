from django.urls import path
from store import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
# from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet)
# router.register('items', views.CartItemViewSet, basename='i   tems')


product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_routers = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_routers.register('items', views.CartItemViewSet, basename='cart-items')


"""collection_router = routers.NestedDefaultRouter(router, 'collections', lookup='collection')
collection_router.register('reviews', views.ReviewSerializer, basename='collection-reviews')"""
"""pprint(router.urls)   --> [<URLPattern '^product/$' [name='product-list']>,
                            <URLPattern '^product/(?P<pk>[^/.]+)/$' [name='product-detail']>,
                            <URLPattern '^collection/$' [name='collection-list']>,
                            <URLPattern '^collection/(?P<pk>[^/.]+)/$' [name='collection-detail']>]"""


urlpatterns = router.urls + product_router.urls + cart_routers.urls

# include router.urls when creating own url
"""urlpatterns = [
    path('').include(router.urls)
    # path("product/", views.ProductList.as_view()),  # as_view() --> convert class into regular function
    # path("product/<int:pk>/", views.ProductDetails.as_view()),  # <int:id> only accept integers,
    #
    # path("collection/", views.CollectionList.as_view()),
    # path("collection/<int:pk>", views.CollectionDetail.as_view(), name='collection-detail')

]"""
