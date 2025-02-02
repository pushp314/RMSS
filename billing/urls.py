from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('orders/', views.order_list, name='order_list'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
