from django.urls import path

from .views import (market, detail, view_cart, add_to_cart, checkout,
                    order_confirmation, update_cart, remove_from_cart)

app_name = 'market'

urlpatterns = [
    path('', market, name='market'),
    path('<int:pk>/detail/', detail, name='detail'),
    path('view-cart/', view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', order_confirmation,
         name='order-confirmation'),
    path('update-cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart,
         name='remove_from_cart'),

]
