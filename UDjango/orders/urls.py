from django.urls import path
from .views import (
    order_list,
    order_detail,
    order_create,
    order_update,
    order_delete,
    order_success,
)

urlpatterns = [

    path('', order_list, name='order_list'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('create/', order_create, name='order_create'),
    path('update/<int:order_id>/', order_update, name='order_update'),
    path('delete/<int:order_id>/', order_delete, name='order_delete'),
    path('success/<int:order_id>/', order_success, name='order_success'),
    path('order/<int:order_id>/update/', order_update, name='order_update'),
]
