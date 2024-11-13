from django.urls import path

from .views import (buyer_list, buyer_detail, buyer_create, buyer_update,
                    buyer_delete)


app_name = 'buyers'

urlpatterns = [
    path('', buyer_list, name='buyer_list'),
    path('<int:pk>/', buyer_detail, name='buyer_detail'),
    path('add/', buyer_create, name='buyer_create'),
    path('<int:pk>/update/', buyer_update, name='buyer_update'),
    path('<int:pk>/delete/', buyer_delete, name='buyer_delete'),

]
