from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=[('Starter', 'Starter'), ('Main Course', 'Main Course'), ('Beverage', 'Beverage'), ('Dessert', 'Dessert')])
    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    table_number = models.IntegerField(null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=[('Dine-in', 'Dine-in'), ('Takeaway', 'Takeaway')])
    payment_method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitem_set", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity
