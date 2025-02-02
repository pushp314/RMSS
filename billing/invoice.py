from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas

def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, f"Invoice for {order.customer_name}")
    y = 780
    for item in order.orderitem_set.all():
        p.drawString(100, y, f"{item.menu_item.name} x {item.quantity} - ${item.subtotal()}")
        y -= 20

    p.drawString(100, y, f"Total: ${order.total_price}")
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'invoice_{order.id}.pdf')
