from django import forms
from .models import MenuItem, Order

class AddItemForm(forms.Form):
    item_id = forms.ModelChoiceField(queryset=MenuItem.objects.all(), label="Select Item")
    quantity = forms.IntegerField(min_value=1, label="Quantity")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'table_number', 'order_type', 'payment_method']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'category']
