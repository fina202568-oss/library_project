from django.urls import path
from . import views

urlpatterns = [
    # ===== MAIN PAGES =====
    path('', views.home_page, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('cart/', views.view_cart, name='view_cart'),
    path('order/', views.order_page, name='order_page'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('checkout-success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('today-special/', views.today_special_partial, name='today_special'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('menuitem/<int:pk>/edit/', views.menuitem_edit, name='menuitem_edit'),
    path('menuitem/<int:pk>/delete/', views.menuitem_delete, name='menuitem_delete'),
]
    