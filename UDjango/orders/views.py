from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from buyers.models import Address
from products.models import Product
from .models import Order, OrderItem
from .forms import OrderForm, OrderUpdateForm

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.price = 0

            products = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')

            order_items = []
            insufficient_products = []

            for product_id, quantity in zip(products, quantities):
                product = get_object_or_404(Product, id=product_id)
                try:
                    quantity = int(quantity)
                except ValueError:
                    messages.error(request, "Некорректное количество товара.")
                    return render(request, 'orders/order_form.html', {
                        'order_form': order_form,
                        'products': Product.objects.filter(count__gt=0),
                        'order_items': [],
                    })

                # Проверяем, доступно ли необходимое количество товара
                if product.count < quantity:
                    insufficient_products.append(
                        f"{product.name}. Доступно: {product.count}.")
                else:
                    order_item = OrderItem(order=order, product=product,
                                           quantity=quantity)
                    order_items.append(order_item)
                    order.price += product.price * quantity

            if insufficient_products:
                messages.error(request,
                               f"Недостаточно товара: {', '.join(insufficient_products)}.")
                return render(request, 'orders/order_form.html', {
                    'order_form': order_form,
                    'products': Product.objects.filter(count__gt=0),
                    'order_items': [{'product_id': int(product_id),
                                     'quantity': int(quantity)} for
                                    product_id, quantity in
                                    zip(products, quantities)],
                })

            with transaction.atomic():
                order.save()  # Сохраняем заказ
                for order_item in order_items:
                    order_item.save()  # Сохраняем все элементы заказа

            return redirect('order_success', order_id=order.id)

    else:
        order_form = OrderForm()

    available_products = Product.objects.filter(count__gt=0)
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'products': available_products,
        'order_items': [],
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {
        'order': order,
    })

@login_required
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            # Сохраняем обновленный заказ без коммита, чтобы отдельно обработать адрес
            order = form.save(commit=False)

            # Получаем данные для полей нового адреса
            new_street = form.cleaned_data.get('new_street')
            new_house_number = form.cleaned_data.get('new_house_number')

            if new_street and new_house_number:
                # Проверка, существует ли уже такой адрес
                existing_address = Address.objects.filter(
                    street=new_street, house_number=new_house_number
                ).first()

                if existing_address:
                    # Если адрес существует, привязываем его к заказу и покупателю
                    order.delivery_address = existing_address
                    order.buyer.addresses.add(
                        existing_address)  # Привязываем адрес к покупателю
                    order.buyer.save()  # Сохраняем покупателя с привязанным адресом
                else:
                    # Если адреса нет, создаем новый
                    new_address = Address.objects.create(
                        street=new_street,
                        house_number=new_house_number
                    )
                    # Привязываем новый адрес к заказу и покупателю
                    order.delivery_address = new_address
                    order.buyer.addresses.add(
                        new_address)  # Привязываем адрес к покупателю
                    order.buyer.save()  # Сохраняем покупателя

            else:
                # Устанавливаем адрес доставки, если выбран существующий адрес
                order.delivery_address = form.cleaned_data['delivery_address']

            # Сохраняем заказ с обновленным адресом доставки
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
        # Заполняем форму текущими данными заказа
        form = OrderUpdateForm(instance=order)

    # Передаем список адресов покупателя для отображения в выпадающем списке
    buyer_addresses = order.buyer.addresses.all()

    return render(request, 'orders/order_update.html',
                  {'buyer': form, 'order': order,
                   'buyer_addresses': buyer_addresses})


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html',
                  {'order': order})
