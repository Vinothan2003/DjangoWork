from django.urls import path
from store import views
from rest_framework.routers import SimpleRouter, DefaultRouter
# from pprint import pprint

router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)
"""pprint(router.urls)   --> [<URLPattern '^product/$' [name='product-list']>,
                            <URLPattern '^product/(?P<pk>[^/.]+)/$' [name='product-detail']>,
                            <URLPattern '^collection/$' [name='collection-list']>,
                            <URLPattern '^collection/(?P<pk>[^/.]+)/$' [name='collection-detail']>]"""

urlpatterns = router.urls

# include router.urls when creating own url
"""urlpatterns = [
    path('').include(router.urls)
    # path("product/", views.ProductList.as_view()),  # as_view() --> convert class into regular function
    # path("product/<int:pk>/", views.ProductDetails.as_view()),  # <int:id> only accept integers,
    #
    # path("collection/", views.CollectionList.as_view()),
    # path("collection/<int:pk>", views.CollectionDetail.as_view(), name='collection-detail')

]"""
