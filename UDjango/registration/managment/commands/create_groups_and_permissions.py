# # python manage.py create_groups_and_permissions
#
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from orders.models import Order
# from products.models import Product
# from profiles.models import Profile
#
#
# class Command(BaseCommand):
#     help = 'Создает группы и назначает права'
#
#     def handle(self, *args, **kwargs):
#         # Создаем группы
#         superadmin_group, created = Group.objects.get_or_create(
#             name='SuperAdmin')
#         worker_group, created = Group.objects.get_or_create(name='Worker')
#         operator_group, created = Group.objects.get_or_create(name='Operator')
#         buyer_group, created = Group.objects.get_or_create(name='Buyer')
#
#         # Создание прав
#         product_content_type = ContentType.objects.get_for_model(Product)
#         order_content_type = ContentType.objects.get_for_model(Order)
#         profile_content_type = ContentType.objects.get_for_model(Profile)
#
#         product_create_permission, created = Permission.objects.get_or_create(
#             codename='add_product',
#             name='Can add product',
#             content_type=product_content_type
#         )
#
#         order_create_permission, created = Permission.objects.get_or_create(
#             codename='add_order',
#             name='Can add order',
#             content_type=order_content_type
#         )
#
#         # Права для группы Buyer
#         profile_view_permission, created = Permission.objects.get_or_create(
#             codename='view_profile',
#             name='Can view profile',
#             content_type=profile_content_type
#         )
#
#         profile_change_permission, created = Permission.objects.get_or_create(
#             codename='change_profile',
#             name='Can change profile',
#             content_type=profile_content_type
#         )
#
#         # Назначение прав в группы
#         superadmin_group.permissions.add(
#             *Permission.objects.all())  # полный доступ
#         worker_group.permissions.add(
#             product_create_permission)  # доступ только к продуктам
#         operator_group.permissions.add(
#             order_create_permission)  # доступ к заказам
#         # Для группы Buyer назначаем права на просмотр и изменение профиля
#         buyer_group.permissions.add(profile_view_permission,
#                                     profile_change_permission)
#
#         self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы'))
