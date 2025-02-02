from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Order, OrderItem
from .forms import AddItemForm, OrderForm

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'billing/menu.html', {'items': items})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_summary', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'billing/create_order.html', {'form': form})


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    menu_items = MenuItem.objects.all()
    form = AddItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        item = form.cleaned_data['item_id']
        quantity = form.cleaned_data['quantity']

        # Check if the item already exists in the order
        existing_item = OrderItem.objects.filter(order=order, menu_item=item).first()
        if existing_item:
            # Update quantity if the item already exists in the order
            existing_item.quantity += quantity
            existing_item.save()
        else:
            # Create a new order item
            OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)

        # Recalculate the total price
        order.total_price = sum(item.subtotal for item in order.orderitem_set.all())
        order.save()

        return redirect('order_summary', order_id=order.id)

    return render(request, 'billing/order_summary.html', {
        'order': order,
        'menu_items': menu_items,
        'form': form,
    })


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.customer_name = request.POST.get('customer_name')
        order.table_number = request.POST.get('table_number') or None
        order.order_type = request.POST.get('order_type')
        order.payment_method = request.POST.get('payment_method')

        # Clear previous order items
        order.orderitem_set.all().delete()

        item_ids = request.POST.getlist('items')
        total_price = 0

        for item_id in item_ids:
            menu_item = get_object_or_404(MenuItem, id=item_id)
            order_item = OrderItem.objects.create(order=order, menu_item=menu_item, quantity=1)
            total_price += order_item.subtotal  # Access as property, not method

        order.total_price = total_price
        order.save()
        return redirect('order_summary', order.id)

    menu_items = MenuItem.objects.all()
    selected_items = order.orderitem_set.values_list('menu_item_id', flat=True)
    return render(request, 'billing/edit_order.html', {'order': order, 'menu_items': menu_items, 'selected_items': selected_items})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')

    return render(request, 'billing/delete_order.html', {'order': order})


def order_list(request):
    orders = Order.objects.all().order_by('-timestamp')
    return render(request, 'billing/order_list.html', {'orders': orders})
