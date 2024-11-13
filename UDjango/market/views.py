from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

from market.models import CartItem, Cart
from orders.models import Order, OrderItem
from products.models import Product


# Представление для интернет-магазина.
def market(request):
    products = Product.objects.all()  # Получаем все товары для отображения в магазине
    return render(request, 'market/market.html', {'products': products})


# Карточка товара
def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'market/detail.html',
                  {'product': product})


# Добавление товара в корзину.
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем или создаем корзину для покупателя.
    buyer = request.user
    cart, created = Cart.objects.get_or_create(buyer=buyer)

    # Проверяем, есть ли этот товар в корзине.
    cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                        product=product,
                                                        defaults={
                                                            'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.save()

    return redirect('market:market')


# Представление для просмотра корзины.
@login_required
def view_cart(request):
    cart = Cart.objects.get_or_create(buyer=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)

    cart_data = []

    # Формируем данные для шаблона.
    for item in cart_items:
        cart_data.append({
            'item': item,
            'price': item.product.price * item.quantity
        })

    total_price = cart.get_total_price()

    return render(request, 'market/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_data': cart_data,
    })


@login_required
def update_cart(request, product_id, action):
    cart = Cart.objects.get_or_create(buyer=request.user)[0]
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    return redirect('market:view_cart')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get_or_create(buyer=request.user)[0]
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('market:view_cart')


# Подтверждение заказа.
@login_required
def checkout(request):
    # Получаем пользователя и его корзину
    buyer = request.user
    cart, created = Cart.objects.get_or_create(buyer=buyer)

    # Получаем товары из корзины
    cart_items = CartItem.objects.filter(cart=cart)

    # Проверка, что корзина не пуста
    if not cart_items:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('market:view_cart')

    # Обрабатываем товары в корзине
    order_items = []
    insufficient_products = []

    try:
        # Используем атомарные транзакции для обеспечения атомарности
        with transaction.atomic():
            for item in cart_items:
                product = Product.objects.select_for_update().get(
                    id=item.product.id)
                quantity = item.quantity
                print(product.count)

                # Проверка наличия товара на складе
                if product.count < quantity:
                    insufficient_products.append(
                        f"{product.name} (доступно: {product.count})")
                else:
                    order_items.append(
                        {'product': product, 'quantity': quantity})

            # Проверка на недостаток товаров
            if insufficient_products:
                messages.error(request,
                               f"Недостаточно товара: {', '.join(insufficient_products)}.")
                return redirect('market:view_cart')

            # Создаем заказ
            order = Order.objects.create(buyer=buyer)
            total_price = 0

            # Обработка товаров и создание OrderItem
            for item in order_items:
                print(product.count)
                product = item['product']
                quantity = item['quantity']
                OrderItem.objects.create(order=order, product=product,
                                         quantity=quantity)

                # Обновляем количество товара на складе
                print(product.count)
                product.count -= quantity
                total_price += product.price * quantity

                product.refresh_from_db()
                product.save()
                print(product.count)

            # Обновляем цену заказа
            order.price = total_price
            order.save()

            # Удаляем товары из корзины только если все прошло успешно
            cart_items.delete()
            messages.success(request,
                             f"Корзина очищена после оформления заказа #{order.id}")

    except Exception as e:
        # Если произошла ошибка, откатываем все изменения
        messages.error(request,
                       f"Произошла ошибка при оформлении заказа: {str(e)}")
        return redirect('market:view_cart')

    # После успешного оформления заказа редирект на подтверждение
    return redirect('market:order-confirmation', order_id=order.id)


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'market/order_confirmation.html',
                  {'order': order}
                  )
