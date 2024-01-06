from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import os


@shared_task
def payment_completed(order_id):
    static_root_path = str(settings.STATIC_ROOT)
    css_path = os.path.join(static_root_path, 'css/pdf.css')
    order = Order.objects.get(id = order_id)
    if order:
      try:
       subject = f'My Shop = Invoice no. {order.id}'
       message = 'Please, find attached the invoice for your recent purchase.'
       email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

       html = render_to_string('orders/order/pdf.html', {'order': order})
       out = BytesIO()
       stylesheets = [weasyprint.CSS(css_path)]
       weasyprint.HTML(string = html).write_pdf(out, stylesheets=stylesheets)
       email.attach(f'order_{order.id}.pdf', 
                 out.getvalue(), 
                 'application/pdf')
       email.send()
      except :
        order = Order.objects.get(id = order_id)