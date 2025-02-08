from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('add_item/', views.add_item, name='add_item'),  # New URL for adding items
    path('create_order/', views.create_order, name='create_order'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('orders/', views.order_list, name='order_list'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('login/', auth_views.LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),  # Update URL
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),  # Delete URL
]
