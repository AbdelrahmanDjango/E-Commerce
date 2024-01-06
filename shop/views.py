
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.files.base import ContentFile
from PIL import Image
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver





def product_list(request, category_slug=None):
    # category_slug = الفئة
    category = None
    categories = Category.objects.all()
    # (products) => Choose the product that's only available.
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                     id=id, 
                                   slug=slug, 
                              available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product' : product,
                                                'cart_product_form' : cart_product_form})

# المتلقي، ماذا يتلقى؟ أمر الحفظ، اللي جاي من المنتج
@receiver(post_save, sender=Product)
# هيرجع الداتا -الموديل- واللي اتحفظ فيها، وأي حاجة تانية
def resize_product_image(sender, instance, **kwargs):
# Check if image an empty or not?
    if instance.image:
        image = Image.open(instance.image)
        image = image.resize((200, 200))
        image.save(instance.image.path, quality=90)