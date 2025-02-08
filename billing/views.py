from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Order, OrderItem
from .forms import AddItemForm, OrderForm, MenuItemForm
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'billing/menu.html', {'items': items})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_summary', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'billing/create_order.html', {'form': form})

from django.shortcuts import render, redirect
from .models import MenuItem
from .forms import MenuItemForm

def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to the menu after adding the item
    else:
        form = MenuItemForm()  # Show an empty form when accessing the page

    return render(request, 'billing/add_item.html', {'form': form})  # Render a template


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

@login_required
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

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')

    return render(request, 'billing/delete_order.html', {'order': order})


def order_list(request):
    orders = Order.objects.all().order_by('-timestamp')
    return render(request, 'billing/order_list.html', {'orders': orders})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')  # Redirect to menu page after registration
    else:
        form = UserCreationForm()
    return render(request, 'billing/register.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm

# UPDATE Menu Item
def update_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to menu page after update
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'billing/update_item.html', {'form': form, 'item': item})


# DELETE Menu Item
def delete_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':  # Confirm delete
        item.delete()
        return redirect('menu')

    return render(request, 'billing/delete_item.html', {'item': item})
