from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page
#
# app_name = 'products'
#
# from products.views import products,ProductDetail
#
# urlpatterns = [
#     # path('', cache_page(3600)(products), name='index'),
#     path('', products, name='index'),
#     path('category/<int:id>', products, name='category'),
#     path('page/<int:page>', products, name='page'),
#     path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
# ]
#
#














from django.contrib import admin
from django.urls import path

app_name = 'products'

from products.views import ProductListView, ProductDetail #products

urlpatterns = [
    # path('', products, name='index'),
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:pk>', ProductListView, name='category'),
    path('page/<int:page>', ProductListView, name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]

