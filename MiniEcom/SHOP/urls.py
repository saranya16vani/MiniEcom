from django.urls import path,include
from . import views
from .api import router

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/update/<int:product_id>/", views.product_update, name="product_update"),
    path("products/delete/<int:product_id>/", views.product_delete, name="product_delete"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("recently-viewed/", views.recently_viewed, name="recently_viewed"),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path("api/", include(router.urls)),
]
