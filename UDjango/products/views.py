from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


# @login_required
# @permission_required('products.can_view_product', raise_exception=True)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html',
                  {'products': products})


# @login_required
# @permission_required('products.can_view_product', raise_exception=True)
def product_detail(request, pk):
    # if not request.user.has_perm('products.can_view_product'):
    #     raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html',
                  {'product': product})


# @login_required
# @permission_required('products.can_add_product', raise_exception=True)
def product_create(request):
    # if not request.user.has_perm('products.can_add_product'):
    #     raise PermissionDenied
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


# @login_required
# @permission_required('products.can_change_product', raise_exception=True)
def product_update(request, pk):
    # if not request.user.has_perm('products.can_change_product'):
    #     raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form,
                                                          'product': product})


# @login_required
# @permission_required('products.can_delete_product', raise_exception=True)
def product_delete(request, pk):
    # if not request.user.has_perm('products.can_delete_product'):
    #     raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html',
                  {'product': product})


# Обработчик исключений для перехвата PermissionDenied и генерации Http404
def permission_denied(request, exception):
    raise Http404  # Отправить на страницу 404, скрывая информацию о странице


# # Новое представление для интернет-магазина
# def market(request):
#     products = Product.objects.all()  # Получаем все товары для отображения в магазине
#     return render(request, 'market/market.html', {'products': products})