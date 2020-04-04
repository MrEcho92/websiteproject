from django.contrib import admin
from django.urls import path
from . import views
from myshop.views import OrderSummaryView


app_name = 'myshop'

urlpatterns= [
    path('product/', views.product_list, name='product_list'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('<category_slug>/',views.product_list, name ='product_list_by_category'),
    path('product/<slug:slug>/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<slug>/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<slug>/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-product-from-cart/<slug>/<int:id>/', views.remove_single_product_from_cart, name='remove_single_product_from_cart'),

]
