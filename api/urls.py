from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.get_products, name="get_products"),
    path("collections/", views.get_collections, name="get_collections"),
    path("faqs/", views.get_faqs, name="get_faqs"),
    path("settings/", views.get_settings, name="get_settings"),
    path("orders/", views.create_order, name="create_order"),
    path("orders/history/", views.order_history, name="order_history"),
    path("contact/", views.create_contact, name="create_contact"),

    # Admin Panel CRUD routes
    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/logout/", views.admin_logout, name="admin_logout"),
    path("admin/stats/", views.admin_stats, name="admin_stats"),
    path("admin/products/", views.admin_products, name="admin_products"),
    path("admin/products/<str:product_id>/", views.admin_product_detail, name="admin_product_detail"),
    path("admin/collections/", views.admin_collections, name="admin_collections"),
    path("admin/collections/<str:collection_id>/", views.admin_collection_detail, name="admin_collection_detail"),
    path("admin/orders/", views.admin_orders, name="admin_orders"),
    path("admin/orders/<int:order_id>/", views.admin_order_detail, name="admin_order_detail"),
    path("admin/messages/", views.admin_messages, name="admin_messages"),
    path("admin/messages/<int:msg_id>/", views.admin_message_detail, name="admin_message_detail"),
    path("admin/settings/", views.admin_settings, name="admin_settings"),
    path("admin/faqs/", views.admin_faqs, name="admin_faqs"),
    path("admin/faqs/<str:faq_id>/", views.admin_faq_detail, name="admin_faq_detail"),
]
