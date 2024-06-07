from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('browse/', views.browse_books, name='browse_books'),
    path('search/', views.search_books, name='search_books'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('inventory/', views.manage_inventory, name='manage_inventory'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]

urlpatterns += [
    path('sales_report/', views.sales_report, name='sales_report'),
    path('inventory_report/', views.inventory_report, name='inventory_report'),
    path('user_activity_report/', views.user_activity_report, name='user_activity_report'),
]
