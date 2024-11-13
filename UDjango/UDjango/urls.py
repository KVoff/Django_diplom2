"""
URL configuration for UDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from employee.views import employee_login_view
from buyers.views import buyer_login_view
from registration.views import register
from django.contrib.auth import views as auth_views
from products.views import permission_denied

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='main'),

    path('admin/', admin.site.urls),

    path('register/', register, name='register'),
    path('login/employee/', employee_login_view, name="employee_login"),
    path("login/buyers/", buyer_login_view, name="buyers_login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('buyers/', include('buyers.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('profiles/', include('profiles.urls')),
    path('market/', include('market.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'products.views.permission_denied'
